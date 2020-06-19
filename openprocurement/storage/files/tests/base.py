import os
import unittest
import webtest
import shutil


class BaseWebTest(unittest.TestCase):

    """Base Web Test to test openprocurement.api.

    It setups the database before each test and delete it after.
    """

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
