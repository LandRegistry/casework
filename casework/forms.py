# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError, Regexp
from ukpostcodeutils.validation import is_valid_postcode
import geojson
import utils
import re

def validate_extent(form, field):
    try:
        extents = geojson.loads(field.data)
    except ValueError:
        raise ValidationError('Valid GeoJSON is required')

    if not extents.get('geometry', False):
        raise ValidationError('A valid geometry type is required')

    if not extents['geometry'].get('type', None) in ['Polygon', 'MultiPolygon']:
        raise ValidationError('A polygon or multi-polygon is required')

    try:
        crs = extents['crs']['properties']['name']
        if not utils.validate_ogc_urn(crs):
            raise ValidationError("A valid 'CRS' containing an EPSG is required")

    except KeyError:
        raise ValidationError("A valid 'CRS' is required")


def validate_postcode(form, field):
    clean = field.data.replace(' ', '').upper()
    if not is_valid_postcode(clean):
        raise ValidationError('Not a valid UK postcode')

def validate_price_paid(form, field):
    regex = '^(£?)?[0-9]+(,[0-9]+)?(\.\d{1,2})?$'
    if field:
        if not re.match(regex, str(field.data)):
            raise ValidationError('Please enter the price paid as pound and pence')

class RegistrationForm(Form):

    """
    The names of the variables here MUST match the name attribute of the fields
    in the index.html for WTForms to work
    Nope: you just have to use the form object you pass to the template and use
    the form object to do the work for you
    """

    title_number = HiddenField('Title Number')
    first_name1 = StringField('First name 1', validators=[DataRequired()])
    surname1 = StringField('Surname 1', validators=[DataRequired()])
    first_name2 = StringField('First name 2')
    surname2 = StringField('Surname 2')

    house_number = StringField('House number', validators=[DataRequired()])
    road = StringField('Road', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired(), validate_postcode])

    property_tenure = RadioField(
      'Property tenure',
      choices=[
        ('Freehold','Freehold'),
        ('Leasehold','Leasehold')
      ]
    )

    property_class = RadioField(
      'Property class',
      choices=[
        ('Absolute','Absolute'),
        ('Good','Good'),
        ('Qualified','Qualified'),
        ('Possessory','Possessory')
      ]
    )

    price_paid = DecimalField(
                    'Price paid (&pound;)',
                    validators=[Optional(), validate_price_paid],
                    places=2,
                    rounding=None)

    extent = TextAreaField('GeoJSON', validators=[DataRequired(), validate_extent])
