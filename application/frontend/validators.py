# -*- coding: utf-8 -*-

from datetime import date

from pytz import timezone
from wtforms.validators import ValidationError


class ValidateDateNotInFuture(object):
    def __init__(self):
        self.message = "The date must not be in the future"

    def __call__(self, form, date_field):
        if date_field.data > date.today():
            raise ValidationError('Date cannot be in the future')


def convert_to_bst(dt):
    utc = timezone('UTC').localize(dt)
    bst = timezone('Europe/London').localize(dt)
    return bst + (utc - bst)

