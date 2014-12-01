import unittest
from application.frontend.frontend import app
from application import db


class CaseworkTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True,
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'testing-not-a-secret'
        db.create_all()
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_check_server(self):

        rv = self.client.get('/pagedoesnotexist')
        self.assertEqual(rv.status, '404 NOT FOUND')

        rv = self.client.get('/')
        self.assertTrue(rv.status in ('200 OK', '302 FOUND'))

    def test_health(self):
        response = self.client.get('/health')
        self.assertEquals(response.status, '200 OK')
