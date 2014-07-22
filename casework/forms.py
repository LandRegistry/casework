from flask_wtf import Form
from wtforms import StringField, RadioField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional

class RegistrationForm(Form):

    """
    The names of the variables here MUST match the name attribute of the fields
    in the index.html for WTForms to work
    Nope: you just have to use the form object you pass to the template and use
    the form object to do the work for you
    """

    title_number = StringField('Title Number')
    first_name1 = StringField('First name 1', validators=[DataRequired()])
    surname1 = StringField('Surname 1', validators=[DataRequired()])
    first_name2 = StringField('First name 2')
    surname2 = StringField('Surname 2')

    house_number = StringField('House number', validators=[DataRequired()])
    road = StringField('Road', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])

    property_tenure = RadioField(
      'Property tenure',
      choices=[
        ('freehold','Freehold'),
        ('leasehold','Leasehold')
      ]
    )

    property_class = RadioField(
      'Property class',
      choices=[
        ('absolute','Absolute'),
        ('good','Good'),
        ('qualified','Qualified'),
        ('possessory','Possessory')
      ]
    )

    price_paid = DecimalField('Price paid (&pound;)', [Optional(),NumberRange(min=0, message='please enter a positive number')], places=2, rounding=None)
