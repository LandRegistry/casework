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

    def test_post_casework_returns_200_and_get_casework_returns_posted_check(self):
        casework_response = self.client.get('/casework')
        self.assertEquals(casework_response.status_code, 200)

        # valid
        casework_response = self.client.post('/casework',
                                             data='{"title_number":"DN1001", "application_type": "Change name"}',
                                             content_type='application/json')

        self.assertEquals(casework_response.status_code, 200)

        # make sure we can see the thing we just created
        casework_response = self.client.get('/casework')
        self.assertEquals(casework_response.status_code, 200)
        self.assertTrue('DN1001' in casework_response.data)
        self.assertTrue('Change name' in casework_response.data)


    def test_post_casework_returns_400_when_invalid_data(self):
        casework_response = self.client.post('/casework',
                                             data='{"XX":"DN1001", "XX": "Change name"}',
                                             content_type='application/json')

        self.assertEquals(casework_response.status_code, 400)

    def test_post_casework_returns_400_when_missing_data(self):
        casework_response = self.client.post('/casework',
                                             data='{"title_number":null, "application_type": null}',
                                             content_type='application/json')

        self.assertEquals(casework_response.status_code, 400)