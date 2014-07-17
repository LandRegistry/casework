import os
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class RegistrationForm(Form):
    titleNumber = TextField('titleNumber', validators=[DataRequired()])
    
