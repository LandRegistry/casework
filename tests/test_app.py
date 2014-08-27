import unittest
import datetime
import json

from wtforms.validators import ValidationError

from application.frontend.frontend import app
from application import db
from application.frontend.forms import RegistrationForm, ChargeForm
from geo_json_fixtures import valid_geo_json, invalid_geo_point


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
        rv = self.client.get('/registration')
        self.assertEquals(rv.status, '200 OK')

        rv = self.client.get('/pagedoesnotexist')
        self.assertEqual(rv.status, '404 NOT FOUND')

        rv = self.client.get('/')
        self.assertEqual(rv.status, '200 OK')

    def test_geojson(self):
        with self.app.test_request_context():
            form = RegistrationForm()

            form.extent.data = ''
            form.validate()
            self.assertEqual(form.extent.errors[0], 'This field is required.')

            # valid data is valid
            form.extent.data = json.dumps(valid_geo_json)
            form.validate()
            self.assertFalse(form.extent.errors)

            # test cannot validate a point
            form.extent.data = invalid_geo_point
            form.validate()
            self.assertEqual(form.extent.errors[0], 'Valid GeoJSON is required')

            # handles an integer accidentally added as geoJSON.
            form.extent.data = '120'
            form.validate()
            self.assertEqual(form.extent.errors[0], 'Valid GeoJSON is required')

            # handles a string accidentally added as geoJSON.
            form.extent.data = 'foo'
            form.validate()
            self.assertEqual(form.extent.errors[0], 'Valid GeoJSON is required')

    def get_valid_create_form_without_charge(self):
        with self.app.test_request_context():
            form = RegistrationForm()

            form.title_number.data = "TEST1234"
            form.first_name1.data = "Kurt"
            form.surname1.data = "Cobain"
            form.first_name2.data = "Courtney"
            form.surname2.data = "Love"

            form.house_number.data = '101'
            form.road.data = "Lake Washington Bldv E"
            form.town.data = "Seattle"
            form.postcode.data = 'SW1A1AA'

            form.property_tenure.data = "Freehold"
            form.property_class.data = "Absolute"
            form.price_paid.data = "1000000"
            form.extent.data = json.dumps(valid_geo_json)

            return form

    def get_valid_create_form_with_charge(self):
        with self.app.test_request_context():
            form = RegistrationForm()

            form.title_number.data = "TEST1234"
            form.first_name1.data = "Kurt"
            form.surname1.data = "Cobain"
            form.first_name2.data = "Courtney"
            form.surname2.data = "Love"

            form.house_number.data = '101'
            form.road.data = "Lake Washington Bldv E"
            form.town.data = "Seattle"
            form.postcode.data = 'SW1A1AA'

            form.property_tenure.data = "Freehold"
            form.property_class.data = "Absolute"
            form.price_paid.data = "1000000"

            charge_form = ChargeForm()
            charge_form.chargee_name.data = "Company 1"
            charge_form.charge_date.data = datetime.datetime.strptime("01-02-2001", "%d-%m-%Y")
            charge_form.chargee_address.data = "21 The Street Plymouth UK PL1 1AA"
            charge_form.chargee_registration_number.data = "1234567"
            form.charges = [charge_form]

            form.extent.data = json.dumps(valid_geo_json)

            return form

    def test_postcode_validation(self):
        form = self.get_valid_create_form_with_charge()
        form.postcode.data = 'XXXXX'
        self.assertFalse(form.validate())

        form.postcode.data = 'SW1A1AA'
        self.assertTrue(form.validate())

    def test_create_form(self):
        form = self.get_valid_create_form_with_charge()
        self.assertTrue(form.validate())

    def test_health(self):
        response = self.client.get('/health')
        self.assertEquals(response.status, '200 OK')

    def test_validate_price_paid(self):
        form = self.get_valid_create_form_with_charge()

        try:
            form.price_paid.data = '20000.19'
            form.validate()
        except Exception as e:
            self.fail("Should not have thrown exception for price " + form.price_paid.data + ' ' + repr(e))

        try:
            form.price_paid.data = '20000.103'
            form.validate()
        except ValidationError as e:
            assert e.message == 'Please enter the price paid as pound and pence'

    def casework(self):
        casework_response = self.client.get('/casework')
        self.assertEquals(casework_response.status_code, 200)

        # valid
        casework_response = self.client.post('/casework',
                                             data='{"title_number":"DN1001", "application_type": "Change name"}',
                                             content_type='application/json')

        self.assertEquals(casework_response.status_code, 200)

        # make sure we can see the thing we just created
        casework_response = self.client.get('/casework')
        self.assertEqual(casework_response.status_code, 200)
        self.assertTrue('DN1001' in casework_response.data)
        self.assertTrue('Change name' in casework_response.data)

        # invalid keys
        casework_response = self.client.post('/casework',
                                             data='{"XX":"DN1001", "XX": "Change name"}',
                                             content_type='application/json')

        self.assertEquals(casework_response.status_code, 400)

        # invalid data
        # TODO: need to make this work
        # casework_response = self.client.post('/casework',
        # data='{"title_number":null, "application_type": null}',
        # content_type='application/json')
        #
        # self.assertEquals(casework_response.status_code, 400)

    def test_checks(self):
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

        # invalid keys
        checks_response = self.client.post('/checks',
                                           data='{"XX":"DN1001", "XX": "Change name"}',
                                           content_type='application/json')

        self.assertEquals(checks_response.status_code, 400)

        # invalid data
        # TODO: need to make this work
        # checks_response = self.client.post('/checks',
        # data='{"title_number":null, "application_type": null}',
        # content_type='application/json')
        #
        # self.assertEquals(checks_response.status_code, 400)

    def test_charge_data(self):
        form = self.get_valid_create_form_with_charge()
        self.assertTrue(form.validate())
