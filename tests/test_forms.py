import datetime
import unittest
import json

from application.frontend.frontend import app
from application.frontend.forms import RegistrationForm, ChargeForm, LeaseholdForm, EasementForm
from geo_json_fixtures import valid_geo_json


class FormsTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True,
        self.app = app
        self.client = app.test_client()

    def test_validate_form_is_true_when_form_is_valid(self):
        with self.app.test_request_context():
            form = RegistrationForm()

            form.title_number.data = "TEST1234"
            form.full_name1.data = "Kurt Cobain"
            form.full_name2.data = "Courtney Love"

            form.address_line_1.data = '101 Lake Washington Bldv E'
            form.address_line_2.data = "line2"
            form.city.data = "Seattle"
            form.postcode.data = 'SW1A1AA'
            form.country.data = 'GB'

            form.property_tenure.data = "Freehold"
            form.property_class.data = "Absolute"
            form.price_paid.data = "10000.00"
            form.price_paid.raw_data = "10000.00"

            form.extent.data = json.dumps(valid_geo_json)
            self.assertTrue(form.validate())

    def test_validate_leasehold_form_contains_errors_for_all_missing_required_fields(self):
        with self.app.test_request_context():
            lease = LeaseholdForm()
            self.assertFalse(lease.validate())

            self.assertEquals(lease.lease_date.errors[0], 'This field is required.')
            self.assertEquals(lease.lease_term.errors[0], 'This field is required.')
            self.assertEquals(lease.lease_from.errors[0], 'This field is required.')
            self.assertEquals(lease.lessor_name.errors[0], 'This field is required.')
            self.assertEquals(lease.lessee_name.errors[0], 'This field is required.')


    def test_form_contains_errors_for_all_missing_required_fields(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            self.assertFalse(form.validate())
            self.assertEquals(form.full_name1.errors[0], 'This field is required.')
            self.assertEquals(form.full_name2.errors, [])
            self.assertEquals(form.address_line_1.errors[0], 'This field is required.')
            self.assertEquals(form.city.errors[0], 'This field is required.')
            self.assertEquals(form.postcode.errors[0], 'This field is required.')
            self.assertEquals(form.country.errors, [])
            self.assertEquals(form.property_tenure.errors[0], 'Not a valid choice')
            self.assertEquals(form.property_class.errors[0], 'Not a valid choice')
            self.assertEquals(form.price_paid.errors, [])
            self.assertEquals(form.charges.errors, [])
            self.assertEquals(form.easements.errors, [])
            self.assertEquals(form.extent.errors[0], 'This field is required.')
            self.assertEquals(form.leases.errors, [])


    def test_validate_extent_raise_validation_error_when_bad_data(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.extent.data = '{"bad":"not a valid thing"}'
            form.validate()
            self.assertEquals(form.extent.errors[0], 'Valid GeoJSON is required')

    def test_validate_extent_raise_validation_error_when_bad_geometry_data(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.extent.data = '{"type": "Feature","geometry": {"type": "Point","coordinates": [125.6, 10.1]},"properties": {"name": "Dinagat Islands"}}'
            form.validate()
            self.assertEquals(form.extent.errors[0], 'Valid GeoJSON is required')


    def test_postcode_validation_contains_error_when_bad_postcode(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.postcode.data = 'XXXXX'
            form.validate()
            self.assertEquals(form.postcode.errors[0], 'Postcode should be a valid UK postcode')

    def test_post_code_has_no_errors_when_price_paid_is_valid(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            form.price_paid.data = '20000.19'
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

    def create_valid_leasehold_form(self):
        form = LeaseholdForm()
        form.lease_date.data = datetime.date.today()
        form.lease_term.data = 10
        form.lease_from.data = datetime.date.today()
        form.lessee_name.data = 'Bob Jones'
        form.lessor_name.data = 'Jo Blow'
        form.lease_easements.data = True
        form.alienation_clause.data = True
        form.title_registered.data = True
        return form

    def test_leasehold_form_validation_for_valid_form(self):
        with self.app.test_request_context():
            form = self.create_valid_leasehold_form()
            self.assertTrue(form.validate())

    def test_leasehold_form_lease_term_less_than_7_or_greater_than_999(self):
        with self.app.test_request_context():
            form = self.create_valid_leasehold_form()
            form.lease_term.data = 6
            self.assertFalse(form.validate())
            self.assertEquals(form.lease_term.errors[0], "Number must be between 7 and 999.")

            form.lease_term.data = 1000
            self.assertFalse(form.validate())
            self.assertEquals(form.lease_term.errors[0], "Number must be between 7 and 999.")

            form.lease_term.data = 7
            self.assertTrue(form.validate())

            form.lease_term.data = 999
            self.assertTrue(form.validate())

    def test_leasehold_form_lease_date_is_not_in_the_future(self):
        with self.app.test_request_context():
            form = self.create_valid_leasehold_form()
            form.lease_date.data =  (datetime.datetime.today() + datetime.timedelta(days=1)).date()
            self.assertFalse(form.validate())
            self.assertEquals(form.lease_date.errors[0], "Date cannot be in the future")

            form.lease_date.data =  datetime.date.today()
            self.assertTrue(form.validate())

    def test_charge_form_is_valid(self):
        with self.app.test_request_context():
            charge_form = ChargeForm()
            charge_form.chargee_name.data = "Company 1"
            charge_form.charge_date.data = datetime.date.today()
            charge_form.chargee_address.data = "21 The Street Plymouth UK PL1 1AA"
            charge_form.chargee_registration_number.data = "1234567"
            charge_form.has_restriction.data = False

            self.assertTrue(charge_form.validate())

    def test_validate_charge_form_contains_errors_for_all_missing_required_fields(self):
        with self.app.test_request_context():
            charge_form = ChargeForm()
            self.assertFalse(charge_form.validate())

            self.assertEquals(charge_form.charge_date.errors[0], 'This field is required.')
            self.assertEquals(charge_form.chargee_name.errors[0], 'This field is required.')
            self.assertEquals(charge_form.chargee_address.errors[0], 'This field is required.')
            self.assertEquals(charge_form.chargee_registration_number.errors[0], 'This field is required.')

    def test_validate_easement_form_is_true_when_form_is_valid(self):
        with self.app.test_request_context():
            easement = EasementForm()
            easement.easement_description.data = "some descr"
            easement.easement_geometry.data = json.dumps(valid_geo_json)
            self.assertTrue(easement.validate())

    def test_validate_easement_form_contains_errors_for_all_missing_required_fields(self):
        with self.app.test_request_context():
            easement = EasementForm()
            self.assertFalse(easement.validate())

            self.assertEquals(easement.easement_description.errors[0], 'This field is required.')
            self.assertEquals(easement.easement_geometry.errors[0], 'This field is required.')

    def test_validate_easement_form_contains_errors_when_geojson_is_not_valid(self):
        with self.app.test_request_context():
            easement = EasementForm()
            easement.easement_description.data = 'some description'
            easement.easement_geometry.data = '{"type": "Feature","geometry": {"type": "Point","coordinates": [125.6, 10.1]},"properties": {"name": "Dinagat Islands"}}'

            self.assertFalse(easement.validate())
            self.assertEquals(easement.easement_geometry.errors[0], 'Valid GeoJSON is required')
            self.assertEquals(easement.easement_description.errors, [])
