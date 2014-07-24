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


    def check_view_registration(self):
        rv = self.client.get('/registration')

        assert rv.status == '200 OK'

    # @mock.patch('casework.mint.Mint.post', return_value=mock_mint_response)
    # def check_create_registration(self, mock_post):
    #     data = dict(
    #                 title_number='TEST1234',
    #                 first_name1='John',
    #                 surname1='Smith',
    #                 first_name2='John',
    #                 surname2='Jone',
    #                 house_number='2',
    #                 road='Highstreet',
    #                 town='New Town',
    #                 postcode='sw1a1aa',
    #                 property_tenure='freehold',
    #                 property_class='good',
    #                 price_paid=1234.12
    #                )
    #
    #     #post data and check that we get a 200
    #     rv = self.app.post('/registration', data=data,follow_redirects=True)
    #     assert rv.status == '200 OK'
    #
    #     #check the there is a link in the page with the correct url
    #     assert '/property/%s' % 'TEST1234' in rv.data

    # @mock.patch('casework.mint.Mint.post', return_value=mock_mint_response)
    # def check_fail_registration(self, mock_post):
    #     data = dict()
    #     rv = self.app.post('/registration', data=data,follow_redirects=True)
    #     assert 'Please review the errors below' in rv.data

    # def test_registration(self):
    #     self.check_view_registration()
    #     self.check_create_registration()
    #     self.check_fail_registration()

    def test_extent(self):
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

            form.property_tenure.data = "Freehold"

            form.property_class.data = "Absolute"

            form.price_paid.data = "1000000"

            form.extent.data = '{ "type": "Feature", "geometry": { "type": "Point", "coordinates": [125.6, 10.1] }, "properties": { "name": "Dinagat Islands" } }'

            valid = form.validate()
            assert valid

        #add some data

        #run validate and assert is true


    def test_404(self):
        rv = self.client.get('/pagedoesnotexist')
        assert rv.status == '404 NOT FOUND'

    def test_view_index(self):
        rv = self.client.get('/')
        assert rv.status == '200 OK'
