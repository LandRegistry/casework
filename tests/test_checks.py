import unittest
from application.frontend.frontend import app
from application import db


class CheckTestCase(unittest.TestCase):
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

    def test_post_checks_returns_200_and_get_checks_returns_posted_check(self):
        checks_response = self.client.get('/checks')
        self.assertEquals(checks_response.status_code, 200)

        # valid
        checks_response = self.client.post('/checks',
                                           data='{"title_number":"DN1001", "application_type": "Change name"}',
                                           content_type='application/json')

        self.assertEquals(checks_response.status_code, 200)

        # make sure we can see the thing we just created
        checks_response = self.client.get('/checks')
        self.assertEquals(checks_response.status_code, 200)
        self.assertTrue('DN1001' in checks_response.data)
        self.assertTrue('Change name' in checks_response.data)


    def test_post_checks_returns_400_when_invalid_data(self):
        checks_response = self.client.post('/checks',
                                           data='{"XX":"DN1001", "XX": "Change name"}',
                                           content_type='application/json')

        self.assertEquals(checks_response.status_code, 400)

    def test_post_checks_returns_400_when_missing_data(self):
        # invalid data
        checks_response = self.client.post('/checks',
                                           data='{"title_number":null, "application_type": null}',
                                           content_type='application/json')

        self.assertEquals(checks_response.status_code, 400)