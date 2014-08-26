import unittest
from flask_security.utils import encrypt_password

from application.frontend.frontend import app
from application import db, user_datastore


class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True,
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'testing-not-a-secret'
        app.config['PROPERTY_FRONTEND_URL'] = 'http://0.0.0.0:8002'
        app.config['MINT_URL'] = 'http://0.0.0.0:8001'
        db.create_all()
        self.app = app.test_client()

        with app.test_request_context():
            user_datastore.create_user(email='caseworker@example.org',
                                           password=encrypt_password('dummypassword'))
            db.session.commit()


    def _login(self, email=None, password=None):
        email = email
        password = password or 'password'
        return self.app.post('/login', data={'email': email, 'password': password},
                             follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_registration_returns_new_title_number(self):
        with app.app_context():
            resp = self._login('caseworker@example.org', 'dummypassword')

            self.assertEqual(200, resp.status_code)

            response = self.app.get('/registration')
            self.assertEqual(200, response.status_code)
            self.assertTrue('Create title' in response.data)