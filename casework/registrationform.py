from flask_wtf import Form
from wtforms import TextField, RadioField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(Form):

    """
    The names of the variables here MUST match the name attribute of the fields
    in the index.html for WTForms to work
    Nope: you just have to use the form object you pass to the template and use
    the form object to do the work for you
    """

    title_number = TextField('Title Number')

    first_name1 = TextField('First name 1', validators=[DataRequired()])
    surname1 = TextField('Surname 1', validators=[DataRequired()])
    first_name2 = TextField('First name 2')
    surname2 = TextField('Surname 2')

    house_number = TextField('House number', validators=[DataRequired()])
    road = TextField('Road', validators=[DataRequired()])
    town = TextField('Town', validators=[DataRequired()])
    postcode = TextField('Postcode', validators=[DataRequired()])

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
        ('possesory','Possesory')
      ]
    )

    price_paid = TextField('Price paid', validators=[DataRequired()])

    submit = SubmitField("Submit")

