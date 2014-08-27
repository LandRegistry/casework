# -*- coding: utf-8 -*-

from datetime import date

from pytz import timezone
from wtforms.validators import ValidationError


class ValidateDateNotInFuture(object):
    def __call__(self, form, field):
        validate_date_not_in_future(form, field.data)


def validate_date_not_in_future(form, date_field):
    if date_field > date.today():
        raise ValidationError('Date cannot be in the future')

def convert_to_bst(dt):
    utc = timezone('UTC').localize(dt)
    bst = timezone('Europe/London').localize(dt)
    return bst + (utc - bst)

