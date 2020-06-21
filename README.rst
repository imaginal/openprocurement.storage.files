
.. image:: https://travis-ci.org/openprocurement/openprocurement.storage.files.svg?branch=master
    :target: https://github.com/openprocurement/openprocurement.storage.files

.. image:: https://coveralls.io/repos/openprocurement/openprocurement.storage.files/badge.svg
  :target: https://github.com/openprocurement/openprocurement.storage.files

.. image:: https://img.shields.io/hexpm/l/plug.svg
    :target: https://github.com/openprocurement/openprocurement.storage.files/blob/master/LICENSE.txt


Simple file storage plugin
==========================

for `openprocurement.documentservice <https://github.com/openprocurement/openprocurement.documentservice>`_


Features
--------

* Full support of openprocurement.documentservice api
* Stores uploads by hash, don't used extra disk space for same uploads
* Secure file ids based on secret_key and double hashing
* Restrict uploads by file extension, mime/type, hash lists
* Custom ``Content-Disposition`` header (inline or attachment)
* Can patch openprocurement.documentservice get_url expire time
* File storage can be distributed to several volumes (up to 65k shards)
* Archive selected files to the separate volume by meta info
* Master/slave replicas support (master/master also can be used)
* Fast download through nginx X-Accel-Redirect feature


Settings
--------

All settings are prefixed with `files.*`

See example in `openprocurement/storage/files/tests/tests.ini <https://github.com/openprocurement/openprocurement.storage.files/blob/master/openprocurement/storage/files/tests/tests.ini>`_


Copyright
---------

© 2020 Volodymyr Flonts


License
-------

Apache 2.0
