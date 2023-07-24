from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField, SubmitField, TelField
from wtforms.validators import Length, EqualTo, Email, ValidationError

from .db import get_db

def data_required(form, field):
    if not field.data:
        if field.name == "dob":
            field_name = "Date of Birth"
        elif field.name == "full_name":
            field_name = "Full Name"
        else:
            field_name = field.name
        raise ValidationError(message=f'{field_name.capitalize()} is required.')
    

def length(min=-1, max=-1):

    def _length(form, field):
        if field.name == "full_name":
            field_name = "Full Name"
        else:
            field_name = field.name
        l = field.data and len(field.data) or 0
        if l < min:
            raise ValidationError(message=f'{field_name.capitalize()} must be at least %d characters.' % (min))
        elif max != -1 and l > max:
            raise ValidationError(message=f'{field_name.capitalize()} must be less than %d characters.' % (max+1))

    return _length


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        data_required,
        length(min=4, max=25)
    ])
            
    full_name = StringField('Full Name', [
        data_required
    ])
    dob = DateField('Date of Birth', [
        data_required
    ])
    email = EmailField('Email Address', [
        data_required,
        Email(),
        length(min=6, max=35)
    ])
    contact = TelField('Contact No.', [
        data_required,
        Length(min=10, max=12, message='Invalid contact number')
    ])
    password = PasswordField('New Password', [
        data_required,
    ])
    confirm = PasswordField('Repeat Password', [
        data_required,
        EqualTo('password', message="Passwords doesn't match")
    ])
    submit = SubmitField('Sign Up')
                

class LoginForm(FlaskForm):
    username = StringField('Username', [
        data_required,
        length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        data_required,
    ])
    submit = SubmitField('Log In')
