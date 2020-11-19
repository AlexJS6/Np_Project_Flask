from flask_wtf import Form
from wtforms import SubmitField, RadioField, PasswordField, StringField
from wtforms import validators, ValidationError

class SignupForm(Form):
    firstname = StringField('First Name', [validators.DataRequired('Please enter your first name')])
    lastname = StringField('Last Name', [validators.DataRequired('Please enter your last name')])
    email = StringField('Email Address', [validators.DataRequired(),  validators.Length(min=6, max=35)])#validators.Email(),
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Send') 
