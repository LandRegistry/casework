from wtforms import *
from flask_wtf import Form
from wtforms.validators import DataRequired, Optional
import simplejson
from datatypes import postcode_validator, geo_json_string_validator, price_validator, country_code_validator

from application.frontend.validators import ValidateDateNotInFuture, ValidateEasementWithinExtent
from application.frontend.field_helpers import countries_list_for_selector
from application import app
import logging

class ChargeForm(Form):
    """
    Charge Form
    """

    charge_date = DateField('Charge date', format='%d-%m-%Y', validators=[DataRequired(), ValidateDateNotInFuture()])
    chargee_name = StringField('Company name', validators=[DataRequired()])
    chargee_registration_number = StringField('Company registration number', validators=[DataRequired()])
    chargee_address = TextAreaField('Address', validators=[DataRequired()])


class EasementForm(Form):
    """
    Easement Form
    """
    easement_description = TextAreaField('Easement description', validators=[DataRequired()])
    easement_geometry = TextAreaField('Easement geometry', validators=[DataRequired(), geo_json_string_validator.wtform_validator()])


class LeaseholdForm(Form):
    """
    Leasehold Form
    """

    lease_date = DateField('Date of Lease', format='%d-%m-%Y', validators=[DataRequired(), ValidateDateNotInFuture()])
    lease_term = StringField('Term (years)', validators=[DataRequired()])
    lease_from = DateField('From date', format='%d-%m-%Y', validators=[DataRequired(), ValidateDateNotInFuture()])
    lessee_name = StringField('2. Lessee name(s)', validators=[DataRequired()])
    lessor_name = StringField('1. Lessor name(s)', validators=[DataRequired()])

    choices_list = [('easements', 'Lease Easement'), ('alienation', 'Alienation Clause'),
                    ('titleRegistered', 'Landlord\'s title registered')]

    lease_easements = BooleanField('Easements within lease', default=False)
    alienation_clause = BooleanField('Alienation clause', default=False)
    title_registered = BooleanField('Landlord\'s title registered', default=False)


class RegistrationForm(Form):
    """
    The names of the variables here MUST match the name attribute of the fields
    in the index.html for WTForms to work
    Nope: you just have to use the form object you pass to the template and use
    the form object to do the work for you
    """

    title_number = HiddenField()
    full_name1 = StringField('Full name 1', validators=[DataRequired()])
    full_name2 = StringField('Full name 2')

    address_line_1 = StringField('Address line 1', validators=[DataRequired()])
    address_line_2 = StringField('Address line 2', validators=[Optional()])
    address_line_3 = StringField('Address line 3', validators=[Optional()])
    address_line_4 = StringField('Address line 4', validators=[Optional()])
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired(), postcode_validator.wtform_validator()])
    country = SelectField('Country',
                          validators=[DataRequired(), country_code_validator.wtform_validator()],
                          choices=countries_list_for_selector)

    property_tenure = RadioField(
        'Property tenure',
        choices=[
            ('Freehold', 'Freehold'),
            ('Leasehold', 'Leasehold')
        ])

    property_class = RadioField(
        'Property class',
        choices=[
            ('Absolute', 'Absolute'),
            ('Good', 'Good'),
            ('Qualified', 'Qualified'),
            ('Possessory', 'Possessory')
        ])

    price_paid = DecimalField(
        'Price paid (&pound;)',
        validators=[
            Optional(strip_whitespace=True),
            price_validator.wtform_validator(message='Please enter the price paid as pound and pence')
        ],
        places=2,
        rounding=None)

    charges = FieldList(FormField(ChargeForm), min_entries=0)
    charges_template = FieldList(FormField(ChargeForm), min_entries=1)

    easements = FieldList(FormField(EasementForm), min_entries=0)
    easements_template = FieldList(FormField(EasementForm), min_entries=1)

    extent = TextAreaField('GeoJSON', validators=[DataRequired(), geo_json_string_validator.wtform_validator(), ValidateEasementWithinExtent()])

    leases = FieldList(FormField(LeaseholdForm), min_entries=0)
    leases_template = FieldList(FormField(LeaseholdForm), min_entries=1)

    def validate(self):
        old_form_charges_template = self.charges_template
        del self.charges_template
        old_form_easements_template = self.easements_template
        del self.easements_template
        old_form_leases_template = self.leases_template
        del self.leases_template
        form_is_validated = super(RegistrationForm, self).validate()
        self.charges_template = old_form_charges_template
        self.easements_template = old_form_easements_template
        return form_is_validated

    def to_dict(self):
        charges = []
        easements = []
        leases = []

        for charge in self['charges'].data:
            dt = charge.pop('charge_date')
            charge['charge_date'] = str(dt)
            charges.append(charge)

        for easement in self['easements'].data:
            geo = easement.pop('easement_geometry')
            easement['easement_geometry'] = simplejson.loads(geo)
            easements.append(easement)

        for lease in self['leases'].data:
            ld = lease.pop('lease_date')
            lf = lease.pop('lease_from')
            lease['lease_date'] = str(ld)
            lease['lease_from'] = str(lf)
            leases.append(lease)

        price_paid = ''
        if self['price_paid'].data:
            price_paid = str(self['price_paid'].data)

        data = {
            "title_number": self['title_number'].data,

            "proprietors": [
                {
                    "full_name": self['full_name1'].data,

                    },
                {
                    "full_name": self['full_name2'].data,
                    }
            ],

            "property": {
                "address": {
                    "address_line_1": self['address_line_1'].data,
                    "address_line_2": self['address_line_2'].data,
                    "address_line_3": self['address_line_3'].data,
                    "address_line_4": self['address_line_4'].data,
                    "city": self['city'].data,
                    "postcode": postcode_validator.to_canonical_form(self['postcode'].data),
                    "country": self['country'].data
                },
                "tenure": self['property_tenure'].data,
                "class_of_title": self['property_class'].data
            },

            "payment": {
                "price_paid": price_paid,
                "titles": [
                    self['title_number'].data
                ]
            },

            "charges": charges,
            "easements": easements,
            "leases": leases,
            "extent": simplejson.loads(self['extent'].data)
        }

        return data
