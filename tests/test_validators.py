import unittest
from datetime import date, timedelta

from wtforms import ValidationError

from application.frontend.validators import ValidateDateNotInFuture


class FakeField(object):
    def __init__(self, data):
        self.data = data

    def data(self):
        return self.data


class ValidatorsTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = ValidateDateNotInFuture()

    def test_can_validate_date_is_not_in_future(self):
        today = date.today()
        day_in_past = today - timedelta(days=1)
        day_in_future = today + timedelta(days=1)

        try:
            self.validator(None, FakeField(today))
            self.validator(None, FakeField(day_in_past))
        except ValidationError as ve:
            self.fail("Should not have thrown validation error " + repr(ve))

        self.assertRaises(ValidationError, self.validator, None, FakeField(day_in_future))
