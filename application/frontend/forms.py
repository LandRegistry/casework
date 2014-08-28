# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField, HiddenField, TextAreaField, FieldList, DateField, FormField, BooleanField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Optional
import simplejson
from datatypes import postcode_validator, geo_json_string_validator, price_validator

from application.frontend.validators import ValidateDateNotInFuture


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

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
    easement_geometry = TextAreaField('Easement geometry',
                                      validators=[DataRequired(), geo_json_string_validator.wtform_validator()])

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

    title_number = HiddenField('Title Number')
    first_name1 = StringField('First name 1', validators=[DataRequired()])
    surname1 = StringField('Surname 1', validators=[DataRequired()])
    first_name2 = StringField('First name 2')
    surname2 = StringField('Surname 2')

    house_number = StringField('House number', validators=[DataRequired()])
    road = StringField('Road', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired(), postcode_validator.wtform_validator()])

    property_tenure = RadioField(
        'Property tenure',
        choices=[
            ('Freehold', 'Freehold'),
            ('Leasehold', 'Leasehold')
        ]
    )

    property_class = RadioField(
        'Property class',
        choices=[
            ('Absolute', 'Absolute'),
            ('Good', 'Good'),
            ('Qualified', 'Qualified'),
            ('Possessory', 'Possessory')
        ]
    )

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

    leases = FieldList(FormField(LeaseholdForm), min_entries=0)
    leases_template = FieldList(FormField(LeaseholdForm), min_entries=1)

    extent = TextAreaField('GeoJSON', validators=[DataRequired(), geo_json_string_validator.wtform_validator()])

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
            lf = lease.pop('lease_form')
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
                    "first_name": self['first_name1'].data,
                    "last_name": self['surname1'].data
                },
                {
                    "first_name": self['first_name2'].data,
                    "last_name": self['surname2'].data
                }
            ],

            "property": {
                "address": {
                    "house_number": self['house_number'].data,
                    "road": self['road'].data,
                    "town": self['town'].data,
                    "postcode": postcode_validator.to_canonical_form(self['postcode'].data)
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
