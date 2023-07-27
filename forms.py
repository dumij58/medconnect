from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField, SubmitField, TelField, SelectField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, ValidationError
from werkzeug.security import check_password_hash

from .models import db, Patient

def data_required(form, field):
    if not field.data:
        if field.name == "dob":
            field_name = "Date of Birth"
        elif field.name == "full_name":
            field_name = "Full Name"
        elif field.name == "emergency_contact":
            field_name = "Emergency Contact"
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

def check_user(form, field):
    uname = str(form.username.data).lower()
    if Patient.query.filter(Patient.username == uname).first():
        raise ValidationError(message=f"User {uname} already exist.")
    
def check_email(form, field):
    email = form.email.data
    if Patient.query.filter(Patient.email == email).first():
        raise ValidationError(message=f"User with email ({email}) already exist.")

# class PtRegForm(FlaskForm):

class RegistrationForm(FlaskForm):
    # Account creation details
    username = StringField('Username', [
        data_required,
        length(min=4, max=25),
        check_user
    ])
    password = PasswordField('Password', [data_required])
    confirm = PasswordField('Repeat Password', [
        data_required,
        EqualTo('password', message="Passwords doesn't match")
    ])
    # Personal information
    full_name = StringField('Full Name', [data_required])
    gender = SelectField('Gender', [data_required], choices=[('','Not Specified'),('m','Male'),('f','Female')])
    dob = DateField('Date of Birth', [data_required])
    address = StringField('Address', [data_required])
    email = EmailField('Email Address', [
        data_required,
        Email(),
        length(min=6, max=35),
        check_email
    ])
    contact = TelField('Contact No.', [
        data_required,
        Length(min=10, max=12, message='Invalid contact number')
    ])
    emergency_contact = TelField('Emergency Contact No.', [
        data_required,
        Length(min=10, max=12, message='Invalid contact number')
    ])
    medical_history = TextAreaField('Medical History')
    submit = SubmitField('Sign Up')
                
def check_uname(form, field):
    if not Patient.query.filter(Patient.username == field.data).first():
        raise ValidationError(message=f"User {field.data} doesn't exist.")
    
def check_pass(form, field):
    user = Patient.query.filter(Patient.username == form.username.data).first()
    if user:
        if not check_password_hash(user.hash, form.password.data):
            raise ValidationError(message="Incorrect password.")

class LoginForm(FlaskForm):
    username = StringField('Username', [
        data_required,
        length(min=4, max=25),
        check_uname
    ])
    password = PasswordField('Password', [
        data_required,
        check_pass
    ])
    submit = SubmitField('Log In')
