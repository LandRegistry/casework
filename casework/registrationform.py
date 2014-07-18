import os
from flask_wtf import Form
from wtforms import TextField, RadioField
from wtforms.validators import DataRequired

class RegistrationForm(Form):

    """
    The names of the variables here MUST match the name attribute of the fields
    in the index.html for WTForms to work
    """
    titleNumber = TextField('Title Number')

    #Proprietors
    firstName1 = TextField('firstName1', validators=[DataRequired()])
    surname1 = TextField('surname1', validators=[DataRequired()])
    firstName2 = TextField('firstName2')
    surname2 = TextField('surname2')

    # Property details
    houseNumber = TextField('houseNumber', validators=[DataRequired()])
    road = TextField('road', validators=[DataRequired()])
    town = TextField('town', validators=[DataRequired()])
    postcode = TextField('postcode', validators=[DataRequired()])

    #Property Tenure and Class
    propertyTenure = RadioField(
      'propertyTenure',
      choices=[
        ('freehold','Freehold'),
        ('leasehold','Leasehold')
      ]
    )
    propertyClass = RadioField(
      'propertyClass',
      choices=[
        ('absolute','Absolute'),
        ('good','Good'),
        ('qualified','Qualified'),
        ('possesory','Possesory')
      ]
    )

    #Price Paid
    pricePaid = TextField('pricePaid', validators=[DataRequired()])
