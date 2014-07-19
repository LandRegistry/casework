import unittest
import mock
from casework.registrationform import RegistrationForm

from casework.server import app

class CaseworkTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()


#TODO This needs some work asap!

