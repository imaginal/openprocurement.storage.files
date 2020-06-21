
.. image:: https://travis-ci.org/imaginal/openprocurement.storage.files.svg?branch=master
    :target: https://github.com/imaginal/openprocurement.storage.files

.. image:: https://coveralls.io/repos/imaginal/openprocurement.storage.files/badge.svg
  :target: https://github.com/imaginal/openprocurement.storage.files

.. image:: https://img.shields.io/hexpm/l/plug.svg
    :target: https://github.com/imaginal/openprocurement.storage.files/blob/master/LICENSE.txt


Simple file storage plugin
==========================

for `openprocurement.documentservice <https://github.com/openprocurement/openprocurement.documentservice>`_


Features
--------

* Full support of openprocurement.documentservice api
* Store uploads by hash, does not use extra disk space for same uploads
* Secure file ids based on secret_key and double hashing
* Forbid uploads by file extension, mime/type, hash black lists
* Custom Content-Disposition header (inline or attachment)
* Can patch openprocurement.documentservice get_url expire time
* File storage can be distributed to several volumes (sharding)
* Support for archiving of selected files on the separate volume
* Master/slave replicas support (master/master also can be used)
* Fast download through nginx X-Accel-Redirect feature


Settings
--------

All settings are prefixed with `files.*`

See example in `openprocurement/storage/files/tests/tests.ini <https://github.com/imaginal/openprocurement.storage.files/blob/master/openprocurement/storage/files/tests/tests.ini>`_


Copyright
---------

© 2020 Volodymyr Flonts


License
-------

Apache 2.0
