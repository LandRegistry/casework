# -*- coding: utf-8 -*-

import re
from datetime import date

from pytz import timezone
from wtforms.validators import ValidationError
from ukpostcodeutils.validation import is_valid_postcode
import geojson


def validate_ogc_urn(crs):
    """
    Method that validates a OGC (Open Geospatial Consortium) CRS (Co-ordinate
    Reference System) URN (Unique Reference Name). Must be an EPSG (European Petroleum
    Survey Group) code, e.g. EPSG:27700 for British National Grid.
    http://www.opengeospatial.org/ogcUrnPolicy
    """

    pattern = 'urn:ogc:def:crs:EPSG:\d{4,5}'
    return re.match(pattern, crs) is not None


def validate_extent(form, extent):
    try:
        extents = geojson.loads(extent.data)
    except ValueError:
        raise ValidationError('Valid GeoJSON is required')

    if not extents.get('geometry', False):
        raise ValidationError('A valid geometry type is required')

    if not extents['geometry'].get('type', None) in ['Polygon', 'MultiPolygon']:
        raise ValidationError('A polygon or multi-polygon is required')

    try:
        crs = extents['crs']['properties']['name']
        if not validate_ogc_urn(crs):
            raise ValidationError("A valid 'CRS' containing an EPSG is required")

    except KeyError:
        raise ValidationError("A valid 'CRS' is required")


def validate_postcode(form, postcode):
    clean = postcode.data.replace(' ', '').upper()
    if not is_valid_postcode(clean):
        raise ValidationError('Not a valid UK postcode')


class ValidateDateNotInFuture(object):
    def __init__(self):
        self.message = "The date must not be in the future"

    def __call__(self, form, field):
        validate_date_not_in_future(form, field.data)


def validate_date_not_in_future(form, date_field):
    if date_field > date.today():
        raise ValidationError('Date cannot be in the future')


def format_postcode(postcode):
    out = postcode.upper()
    if ' ' not in postcode:
        i = len(postcode) - 3
        out = out[:i] + ' ' + out[i:]

    return out


def convert_to_bst(dt):
    utc = timezone('UTC').localize(dt)
    bst = timezone('Europe/London').localize(dt)
    return bst + (utc - bst)


def validate_price_paid(form, price_paid):
    regex = '^(£?)?[0-9]+(,[0-9]+)?(\.\d{1,2})?$'
    if price_paid:
        if not re.match(regex, str(price_paid.data)):
            raise ValidationError('Please enter the price paid as pound and pence')