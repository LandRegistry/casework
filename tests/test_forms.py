import datetime
import unittest
from application.frontend.frontend import app
from application.frontend.forms import RegistrationForm, ChargeForm


class FormsTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True,
        self.app = app
        self.client = app.test_client()

    def test_valid_create_form_with_charge(self):
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

            form.extent.data = '{   "type": "Feature",   "crs": {     "type": "name",     "properties": {       "name": "urn:ogc:def:crs:EPSG:27700"     }   },   "geometry": {      "type": "Polygon",     "coordinates": [       [ [530857.01, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.01, 181500.00] ]       ]   },   "properties" : {      } }'

            self.assertTrue(form.validate())

    def test_form_contains_errors_for_all_missing_required_fields(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            self.assertFalse(form.validate())
            self.assertEquals(form.first_name1.errors[0], 'This field is required.')
            self.assertEquals(form.surname1.errors[0], 'This field is required.')
            self.assertEquals(form.first_name2.errors, [])
            self.assertEquals(form.surname2.errors, [])
            self.assertEquals(form.house_number.errors[0], 'This field is required.')
            self.assertEquals(form.road.errors[0], 'This field is required.')
            self.assertEquals(form.town.errors[0], 'This field is required.')
            self.assertEquals(form.postcode.errors[0], 'This field is required.')
            self.assertEquals(form.property_tenure.errors[0], 'Not a valid choice')
            self.assertEquals(form.property_class.errors[0], 'Not a valid choice')
            self.assertEquals(form.price_paid.errors, [])
            self.assertEquals(form.charges.errors, [])
            self.assertEquals(form.easements.errors, [])
            self.assertEquals(form.extent.errors[0], 'This field is required.')


    def test_form_extent_contains_an_error_when_geojson_not_populated(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.extent.data = ''
            form.validate()
            self.assertEquals(form.extent.errors[0], 'This field is required.')

    def test_postcode_validation_contains_error_when_bad_postcode(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.postcode.data = 'XXXXX'
            form.validate()
            self.assertEquals(form.postcode.errors[0], 'Postcode should be a valid UK postcode')

    def test_post_code_has_no_errors_when_postcode_is_valid(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.postcode.data = 'SW1A1AA'
            form.validate()
            self.assertEquals(form.postcode.errors, [])

    def test_validate_price_paid_errors_is_empty_when_valid_price(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.price_paid.data = '20000.19'
            form.validate()
            self.assertEquals(form.price_paid.errors, [])

    @unittest.skip("price paid validation is not working at the moment.")
    def test_validate_price_paid_contains_error_when_too_many_decimal_points(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.price_paid.data = '20000.103'
            form.validate()
            self.assertEquals(form.price_paid.errors[0], 'Please enter the price paid as pound and pence')
