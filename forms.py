from wtforms import Form, StringField, PasswordField, DateField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo, Email, ValidationError

def data_required(form, field):
    if not field.data:
        raise ValidationError('Field is required.')
    
def len_check(form, field):
    if len(field.data) < 4:
        raise ValidationError('Username must be more than 4 characters.')
    elif len(field.data) > 25:
        raise ValidationError('Username must be less than 25 characters.')

class RegistrationForm(Form):
    username = StringField('Username', [
        #Length(min=4, max=25),
        len_check,
        data_required
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
        EqualTo('confirm')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', [
        Length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        EqualTo('confirm')
    ])
    confirm = PasswordField('Repeat Password')
