import os
import unittest
import webtest
import shutil
from multiprocessing import Process


def slave_main():
    from openprocurement.documentservice import main
    from gevent.pywsgi import WSGIServer
    from ConfigParser import ConfigParser
    config = os.path.dirname(__file__) + "/tests.ini"
    defaults = dict(here=os.path.dirname(__file__))
    parser = ConfigParser(defaults=defaults)
    parser.read(config)
    settings = dict(parser.items("app:main"))
    settings.pop("files.slave_api")
    app = main({}, **settings)
    server = WSGIServer(('127.0.0.1', 6545), app, log=None)
    server.serve_forever()


class BaseWebTest(unittest.TestCase):

    """Base Web Test to test openprocurement.api.

    It setups the database before each test and delete it after.
    """

    @classmethod
    def setUpClass(cls):
        cls.slave = Process(target=slave_main)
        cls.slave.daemon = True
        cls.slave.start()

    @classmethod
    def tearDownClass(cls):
        cls.slave.terminate()

    def setUp(self):
        self.app = webtest.TestApp(
            "config:tests.ini", relative_to=os.path.dirname(__file__))
        self.app.authorization = ('Basic', ('broker', 'broker'))
        save_path = self.app.relative_to + '/files'
        if os.path.exists(save_path):
            shutil.rmtree(save_path)

    def tearDown(self):
        save_path = self.app.relative_to + '/files'
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
