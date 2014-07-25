import unittest
import mock
import flask
from casework.server import app
from casework.forms import RegistrationForm

class MockMintResponse():
    status_code = 200
    url = 'http://localhost:8000'

mock_mint_response = MockMintResponse()

class CaseworkTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True,
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'testing-not-a-secret'
        self.app = app
        self.client = app.test_client()

    def check_server(self):
        
        rv = self.client.get('/registration')
        assert rv.status == '200 OK'

        rv = self.client.get('/pagedoesnotexist')
        assert rv.status == '404 NOT FOUND'

        rv = self.client.get('/')
        assert rv.status == '200 OK'

    def test_create_form(self):

        with self.app.test_request_context():

            form = RegistrationForm()

            form.title_number.data = "TEST1234"
            form.first_name1.data =  "Kurt"
            form.surname1.data = "Cobain"
            form.first_name2.data = "Courtney"
            form.surname2.data = "Love"

            form.house_number.data = '101'
            form.road.data = "Lake Washington Bldv E"
            form.town.data = "Seattle"
            form.postcode.data = 'TE57 CD3'

            form.property_tenure.data = "freehold"
            form.property_class.data = "absolute"
            form.price_paid.data = "1000000"
            form.extent.data = '{ "type": "Feature", "geometry": { "type": "Point", "coordinates": [125.6, 10.1] }, "properties": { "name": "Dinagat Islands" } }'

            valid = form.validate()
            assert valid
