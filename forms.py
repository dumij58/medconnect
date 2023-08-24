from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, DateField, TimeField, EmailField, SubmitField, TelField, SelectField, TextAreaField, SearchField, FieldList, FormField
from wtforms.validators import Length, EqualTo, Email, ValidationError, Optional
from werkzeug.security import check_password_hash
from datetime import date as d, timedelta

from .helpers import f_age
from .models import db, Patient, Doctor, Admin, Hospital, DocSession

def data_required(form, field):
    if not field.data:
        if field.name == "dob":
            field_name = "Date of Birth"
        elif field.name == "full_name":
            field_name = "Full Name"
        elif field.name == "emergency_contact":
            field_name = "Emergency Contact"
        elif field.name == "old_pass":
            field_name = "Old Password"
        elif field.name == "reg_no":
            field_name = "Registration No."
        elif field.name == "confirm":
            field_name = "Repeat Password"
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
    if Patient.query.filter(Patient.username == uname).first() or Doctor.query.filter(Doctor.username == uname).first():
        raise ValidationError(message=f"User {uname} already exist.")


def check_pass_requirements(form, field):
    pwd = str(field.data)
    noUpper = True
    noLower = True
    noDigit = True
    for i in pwd:
        if i.isupper():
            noUpper = False
        elif i.islower():
            noLower = False
        elif i.isdigit():
            noDigit = False
    if noUpper or noLower or noDigit or len(pwd) < 8:
        raise ValidationError(message=f"Password reqirements not met.")
    

class PtRegForm(FlaskForm):
    # Account creation details
    username = StringField('Username', [
        data_required,
        length(min=4, max=25),
        check_user
    ])
    password = PasswordField('Password', [
        data_required,
        check_pass_requirements
    ])
    confirm = PasswordField('Repeat Password', [
        data_required,
        EqualTo('password', message="Passwords doesn't match")
    ])
    # Personal information
    full_name = StringField('Full Name', [data_required])
    gender = SelectField('Gender', [
        data_required
    ], choices=[('','Select Your Gender'),('m','Male'),('f','Female'),('o','Other')])
    dob = DateField('Date of Birth', [data_required])
    address = StringField('Address', [data_required])
    email = EmailField('Email Address', [
        data_required,
        Email(),
        length(min=6, max=35)
    ])
    contact = TelField('Contact', [
        data_required,
        Length(min=10, max=12, message='Invalid contact number')
    ])
    emergency_contact = TelField('Emergency Contact', [
        data_required,
        Length(min=10, max=12, message='Invalid contact number')
    ])
    submit = SubmitField('Sign Up')


class MedicalHistoryForm(FlaskForm):
    medical_condition = StringField('Medical Condition', validators=[Optional()])
    diagnosis_date = DateField('Diagnosis Date', validators=[Optional()])
    treatment = TextAreaField('Treatment', validators=[Optional()])


class MedicationForm(FlaskForm):
    medication_name = StringField('Medication Name', validators=[Optional()])
    dosage = StringField('Dosage', validators=[Optional()])
    frequency = StringField('Frequency', validators=[Optional()])
    start_date = DateField('Start Date', validators=[Optional()])


class PastSurgeryForm(FlaskForm):
    surgery_name = StringField('Surgery Name', validators=[Optional()])
    date = DateField('Date', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])


class VaccinationForm(FlaskForm):
    vaccine_name = StringField('Vaccine Name', validators=[Optional()])
    administration_date = DateField('Administration Date', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])


class FamilyHistoryForm(FlaskForm):
    relationship = StringField('Relationship', validators=[Optional()])
    medical_condition = StringField('Medical Condition', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])


class AddDetailsForm(FlaskForm):
    medical_history = FieldList(FormField(MedicalHistoryForm), min_entries=1)
    current_medications = FieldList(FormField(MedicationForm), min_entries=1)
    past_surgeries = FieldList(FormField(PastSurgeryForm), min_entries=1)
    vaccinations = FieldList(FormField(VaccinationForm), min_entries=1)
    family_medical_history = FieldList(FormField(FamilyHistoryForm), min_entries=1)
    submit = SubmitField('Go to Profile')


def check_age(form, field):
    age = f_age(form.dob.data)
    if age < 18:
        raise ValidationError(message=f"Doctor must be at least 18 years old.")


class DocRegForm(FlaskForm):
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
    gender = SelectField('Gender', [
        data_required
    ], choices=[('','Not Specified'),('m','Male'),('f','Female'),('o','Other')])
    dob = DateField('Date of Birth', [
        data_required,
        check_age
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
    reg_no = IntegerField('Registration No.', [data_required])
    specializations = StringField('Specializations', [data_required])
    submit = SubmitField('Sign Up')
                

def check_uname(form, field):
    if Patient.query.filter(Patient.username == field.data).first() or \
    Doctor.query.filter(Doctor.username == field.data).first() or \
    Admin.query.filter(Admin.username == field.data).first():
        return
    else:
        raise ValidationError(message=f"User {field.data} doesn't exist.")
    

def check_pass(form, field):
    pt = Patient.query.filter(Patient.username == form.username.data).first()
    doc = Doctor.query.filter(Doctor.username == form.username.data).first()
    admin = Admin.query.filter(Admin.username == form.username.data).first()
    if pt:
        if not check_password_hash(pt.hash, form.password.data):
            raise ValidationError(message="Incorrect password.")
    elif doc:
        if not check_password_hash(doc.hash, form.password.data):
            raise ValidationError(message="Incorrect password.")
    elif admin:
        if not check_password_hash(admin.hash, form.password.data):
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


def check_hospital(form, field):
    name = form.name.data
    if Hospital.query.filter(Hospital.name == name).first():
        raise ValidationError(message=f"Hospital ({name}) already exist.")
    

class HlRegForm(FlaskForm):
    name = StringField('Name', [
        data_required,
        check_hospital
    ])
    address = TextAreaField('Address', [data_required])
    email = EmailField('Email', [
        data_required,
        Email(),
        length(min=6, max=35)
    ])
    contact = TelField('Contact No.', [data_required])
    submit = SubmitField('Add')


def check_date(form, field):
    date = field.data
    if date <= d.today() + timedelta(days=1):
        raise ValidationError(message=f"Select a future date")
    

def check_time_overlap(form, field):
    date = form.date.data
    time = field.data
    st = form.start_t.data
    et = form.end_t.data
    sessions = db.session.execute(db.select(DocSession).where(DocSession.date == date)).scalars()
    for session in sessions:
        # Ensure start and end times of the new session doesn't overlap with existing ones
        if time >= session.start_t and time <= session.end_t:
            if field == form.start_t:
                raise ValidationError(message=f"Start time overlapping with an existing session")
            elif field == form.end_t:
                raise ValidationError(message=f"End time overlapping with an existing session")
            
        elif st <= session.start_t and et >= session.end_t:
            if field == form.end_t:
                raise ValidationError(message=f"Session time overlapping with an existing session")
    

    
class SessionForm(FlaskForm):
    hl_id = SelectField('Hospital', [data_required], coerce=int)
    date = DateField('Date', [
        data_required,
        check_date
    ])
    start_t = TimeField('Start', [
        data_required,
        check_time_overlap
    ])
    end_t = TimeField('End', [
        data_required,
        check_time_overlap
    ])
    submit = SubmitField('Add')


class ApmtSearchForm(FlaskForm):
    doc = SearchField('Doctor', [data_required])
    hl = SearchField('Hospital')
    date = DateField('Date')
    time = TimeField('Time')
    submit = SubmitField('Search')


class ChangePassForm(FlaskForm):
    old_pass = PasswordField('Old Password', [data_required])
    password = PasswordField('New Password', [data_required])
    confirm = PasswordField('Repeat Password', [
        data_required,
        EqualTo('password', message="Passwords doesn't match")
    ])
    submit = SubmitField('Change Password')


class VitalSigns(FlaskForm):
    sign = StringField('Sign', [Optional()])
    value = StringField('Value', [Optional()])


class ExaminationNotes(FlaskForm):
    title = StringField('Title', [Optional()])
    notes = TextAreaField('Notes', [Optional()])


class ExaminationForm(FlaskForm):
    chief_complaint = TextAreaField('Chief Complaint', [Optional()])
    vital_signs = FieldList(FormField(VitalSigns), min_entries=1)
    examination_notes = FieldList(FormField(ExaminationNotes), min_entries=1)


class OrderTestForm(FlaskForm):
    test_name = StringField('Test Name', validators=[Optional()])
    test_date = DateField('Test Date', validators=[Optional()])
    additional_notes = TextAreaField('Additional Notes')


class TreatmentsForm(FlaskForm):
    title = StringField('Title', [Optional()])
    treatment_notes = TextAreaField('Treatment Notes', [Optional()]) 


class DiagnosisTreatmentForm(FlaskForm):
    diagnosis = TextAreaField('Diagnosis', [Optional()])
    treatments = FieldList(FormField(TreatmentsForm), min_entries=1)
    medications = FieldList(FormField(MedicationForm), min_entries=1)


class FollowUpForm(FlaskForm):
    follow_up_date = DateField("Date (If Applicable)")
    follow_up_notes = TextAreaField("Notes")


class ExternalDoctorForm(FlaskForm):
    doctor_name = StringField("Doctor's Name")
    specialization = StringField("Specialization")


class ReferralForm(FlaskForm):
    referral_date = DateField('Referral Date')
    doctor = SearchField('Doctor')
    external_doctor = FieldList(FormField(ExternalDoctorForm), min_entries=1)
    reason = StringField('Reason for Referral')
    referral_notes = TextAreaField('Notes')


class ContactForm(FlaskForm):
    name = StringField('Name', [data_required])
    email = EmailField('Email', [
        data_required,
        Email(),
        length(min=6, max=35)
    ])
    message = TextAreaField('Message', [data_required])