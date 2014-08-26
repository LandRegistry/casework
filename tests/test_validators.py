import unittest
from datetime import date, timedelta

from wtforms import ValidationError

from application.frontend.validators import validate_ogc_urn, validate_date_not_in_future


class ValidatorsTestCase(unittest.TestCase):
    def test_validate_ogc_urn(self):
        self.assertTrue(validate_ogc_urn('urn:ogc:def:crs:EPSG:27700'))
        self.assertTrue(validate_ogc_urn('urn:ogc:def:crs:EPSG:1234'))
        self.assertFalse(validate_ogc_urn('XXXXX'))
        self.assertFalse(validate_ogc_urn('urn:ogc:def:crs:XXX::27700'))

    def test_can_validate_date_is_not_in_future(self):
        today = date.today()
        day_in_past = today - timedelta(days=1)
        day_in_future = today + timedelta(days=1)

        try:
            validate_date_not_in_future(None, today)
            validate_date_not_in_future(None, day_in_past)
        except ValidationError as ve:
            self.fail("Should not have thrown validation error " + repr(ve))

        self.assertRaises(ValidationError, validate_date_not_in_future, None, day_in_future)
