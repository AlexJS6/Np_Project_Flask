from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField, RadioField, SelectField, PasswordField

from wtforms import validators, ValidationError

class FlightForm(Form):
    firstname = TextField('First name', [validators.Required('Please enter your first name')])
    lastname = TextField('Last name', [validators.Required('Please enter your last name')])
    email = TextField('Email', [validators.Required('Please enter your email address.'), validators.Email('Please enter your email address.')])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Send') 
