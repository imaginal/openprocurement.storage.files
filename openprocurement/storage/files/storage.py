import os
import os.path
import hashlib
import magic
import zipfile
import simplejson as json
from shutil import copyfileobj
from hmac import compare_digest
from datetime import datetime
from pytz import timezone
from rfc6266 import build_header
from urllib import quote
from openprocurement.storage.files.dangerous import DANGEROUS_EXT, DANGEROUS_MIME_TYPES
from openprocurement.documentservice.storage import (HashInvalid, KeyNotFound, ContentUploaded,
    StorageUploadError, get_filename)


TZ = timezone(os.environ['TZ'] if 'TZ' in os.environ else 'Europe/Kiev')


def get_now():
    return datetime.now(TZ)


class FilesStorage:
    def __init__(self, settings):
        self.web_root = settings['files.web_root'].strip()
        self.save_path = settings['files.save_path'].strip()
        self.secret_key = settings['files.secret_key'].strip()
        self.disposition = settings.get('files.disposition', '') or 'inline'
        dangerous_ext = settings.get('files.dangerous_ext', '') or DANGEROUS_EXT
        self.dangerous_ext = set([s.strip().upper() for s in dangerous_ext.split(',') if s.strip()])
        self.dangerous_mime = DANGEROUS_MIME_TYPES
        self.forbidden_hash = set(['d41d8cd98f00b204e9800998ecf8427e'])
        if 'files.dangerous_mime' in settings:
            with open(settings['files.dangerous_mime']) as fp:
                self.dangerous_mime = set([s.strip().lower() for s in fp.readlines() if '/' in s.strip()])
        if 'files.forbidden_hash' in settings:
            with open(settings['files.forbidden_hash']) as fp:
                self.forbidden_hash = set([s.strip().lower() for s in fp.readlines() if len(s.strip()) == 32])
            self.magic = magic.Magic(mime=True)
        self.dir_mode = 0o2710
        self.file_mode = 0o440
        self.meta_mode = 0o400

    def accel_location(self, uuid):
        return os.path.join(self.web_root, uuid[-2:], uuid[-4:])

    def full_path(self, uuid):
        return os.path.join(self.save_path, uuid[-2:], uuid[-4:])

    def save_meta(self, uuid, meta, overwrite=False):
        path = self.full_path(uuid)
        name = os.path.join(path, uuid + '.meta')
        if not overwrite and os.path.exists(name):
            raise ContentUploaded(uuid)
        meta['modified'] = get_now().isoformat()
        if not os.path.exists(path):
            os.makedirs(path, mode=self.dir_mode)
        with open(name + '~', 'wt') as fp:
            json.dump(meta, fp)
        os.rename(name + '~', name)
        os.chmod(name, self.meta_mode)

    def read_meta(self, uuid):
        path = self.full_path(uuid)
        name = os.path.join(path, uuid + '.meta')
        if not os.path.exists(name):
            raise KeyNotFound(uuid)
        with open(name) as fp:
            return json.load(fp)

    def check_dangerous(self, filename, content_type, fp):
        for ext in filename.rsplit('.', 2)[1:]:
            if ext.upper() in self.dangerous_ext:
                return True
        if content_type.lower() in self.dangerous_mime:
            return True
        fp.seek(0)
        magic_type = self.magic.from_buffer(fp.read(2048))
        if magic_type.lower() in self.dangerous_mime:
            return True
        if filename.upper().endswith('.ZIP') or \
                'application/zip' in (content_type, magic_type):
            fp.seek(0)
            try:
                zipobj = zipfile.ZipFile(fp)
            except zipfile.BadZipfile:
                return
            for filename in zipobj.namelist():
                for ext in filename.rsplit('.', 2)[1:]:
                    if ext.upper() in self.dangerous_ext:
                        return True

    def compute_md5(self, in_file, blocksize=0x10000):
        in_file.seek(0)
        md5hash = hashlib.md5()
        while True:
            block = in_file.read(blocksize)
            if not block or not len(block):
                break
            md5hash.update(block)
        return md5hash.hexdigest()

    def register(self, md5hash):
        if md5hash in self.forbidden_hash:
            raise StorageUploadError('forbidden_file')
        now_iso = get_now().isoformat()
        uuid = hashlib.md5(md5hash + self.secret_key).hexdigest()
        meta = dict(hash=md5hash, created=now_iso)
        try:
            self.save_meta(uuid, meta)
        except ContentUploaded:
            pass
        return uuid

    def upload(self, post_file, uuid=None):
        now_iso = get_now().isoformat()
        filename = get_filename(post_file.filename)
        content_type = post_file.type
        in_file = post_file.file
        md5hash = self.compute_md5(in_file)
        if md5hash in self.forbidden_hash:
            raise StorageUploadError('forbidden_file')

        if uuid is None:
            uuid = hashlib.md5(md5hash + self.secret_key).hexdigest()
            meta = dict(hash=md5hash, created=now_iso)
        else:
            meta = self.read_meta(uuid)
            if not compare_digest(meta['hash'], md5hash):
                raise HashInvalid(md5hash)

        path = self.full_path(uuid)
        name = os.path.join(path, uuid)
        if os.path.exists(name):
            meta = self.read_meta(uuid)
            if meta['filename'] != filename:
                if 'alternatives' not in meta:
                    meta['alternatives'] = list()
                meta['alternatives'].append({
                    'created': now_iso,
                    'filename': filename
                })
                self.save_meta(uuid, meta, overwrite=True)
            return uuid, 'md5:' + md5hash, content_type, filename

        if self.check_dangerous(filename, content_type, in_file):
            raise StorageUploadError('dangerous_file')

        meta['filename'] = filename
        meta['Content-Type'] = content_type
        meta['Content-Disposition'] = build_header(
            filename,
            disposition=self.disposition,
            filename_compat=quote(filename.encode('utf-8')))
        self.save_meta(uuid, meta, overwrite=True)

        in_file.seek(0)
        with open(name + '~', 'wb') as out_file:
            copyfileobj(in_file, out_file)
        os.rename(name + '~', name)
        os.chmod(name, self.file_mode)

        return uuid, 'md5:' + md5hash, content_type, filename

    def get(self, uuid):
        meta = self.read_meta(uuid)
        if meta['hash'] in self.forbidden_hash:
            raise KeyNotFound(uuid)
        path = self.accel_location(uuid)
        meta['X-Accel-Redirect'] = os.path.join(path, uuid).encode()
        return meta
