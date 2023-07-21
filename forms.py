from wtforms import Form, StringField, PasswordField, DateField, EmailField
from wtforms.validators import Length, EqualTo, Email

class RegistrationForm(Form):
    username = StringField('Username', [
        Length(min=4, max=25)
    ])
    full_name = StringField('Full Name', [
    ])
    dob = DateField('Date of Birth', [
    ])
    email = EmailField('Email Address', [
         Email(),
        Length(min=6, max=35)
    ])
    contact = StringField('Contact No.', [
        Length(min=10, max=12)
    ])
    password = PasswordField('New Password', [
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', [
        Length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')