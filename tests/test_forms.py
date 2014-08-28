import datetime
import unittest
import json

from application.frontend.frontend import app
from application.frontend.forms import RegistrationForm, ChargeForm
from geo_json_fixtures import valid_geo_json


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

            form.address_line_1.data = '101 Lake Washington Bldv E'
            form.address_line_2.data = "line2"
            form.address_line_3.data = "line3"
            form.address_line_4.data = "line4"
            form.city.data = "Seattle"
            form.postcode.data = 'SW1A1AA'
            form.country.data = 'GB'

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
            self.assertTrue(form.validate())


    def test_form_contains_errors_for_all_missing_required_fields(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            self.assertFalse(form.validate())
            self.assertEquals(form.first_name1.errors[0], 'This field is required.')
            self.assertEquals(form.surname1.errors[0], 'This field is required.')
            self.assertEquals(form.first_name2.errors, [])
            self.assertEquals(form.surname2.errors, [])
            self.assertEquals(form.address_line_1.errors[0], 'This field is required.')
            self.assertEquals(form.city.errors[0], 'This field is required.')
            self.assertEquals(form.postcode.errors[0], 'This field is required.')
            self.assertEquals(form.country.errors[0], 'Not a valid choice')
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
            form.price_paid.raw_data = '20000.19'
            form.validate()
            self.assertEquals(form.price_paid.errors, [])


    def test_validate_price_paid_contains_errors_when_non_numeric_price(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.price_paid.data = 'sausages'
            form.price_paid.raw_data = 'sausages'  # TODO: Hack. We need to construct forms properly
            form.validate()
            self.assertEquals(form.price_paid.errors[0], 'Please enter the price paid as pound and pence')


    def test_validate_price_paid_contains_error_when_too_many_decimal_points(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.price_paid.data = '20000.103'
            form.price_paid.raw_data = '20000.103'  # TODO: Hack, we need to construct forms properly
            form.validate()
            self.assertEquals(form.price_paid.errors[0], 'Please enter the price paid as pound and pence')




