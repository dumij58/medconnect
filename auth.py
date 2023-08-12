from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for
)
from werkzeug.security import generate_password_hash
from datetime import datetime

from .helpers import login_required
from .models import db, Patient, Doctor, DoctorPreVal, Admin, Log
from .forms import PtRegForm, DocRegForm, LoginForm, AddDetailsForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register/pt', methods=('GET', 'POST'))
def register():
    # Ensure user is not logged in
    if g.user is not None:
        return redirect(url_for('index'))
    
    # Initialize registration form
    form = PtRegForm()

    # Ensure data is validated on submit
    if request.method == 'POST' and form.validate():
        
        # Update database
        new_patient = Patient(
            username = str(form.username.data).lower(),
            hash = generate_password_hash(form.password.data),
            full_name = form.full_name.data,
            gender = form.gender.data,
            dob = form.dob.data,
            email = form.email.data,
            contact = form.contact.data,
            address = form.address.data,
            emergency_contact = form.emergency_contact.data,
            created = datetime.now()
        )
        ## Add records to database and commit all changes
        db.session.add(new_patient)

        # Append a remark to log
        append = Log(
            created = datetime.now(),
            user = form.username.data,
            remarks = f"Patient ({form.username.data}) added to DB"
        )
        db.session.add(append)

        # Commit all changes to database
        db.session.commit()
        
        # Redirect to add patient details page
        # flash('Registration Successful!', "success")
        return redirect(url_for('auth.login'))
    
    # Render the registration form
    return render_template('auth/register.html', form = form)


@bp.route('/register/doc', methods=('GET', 'POST'))
def doc_register():
    # Ensure user is not logged in
    if g.user is not None:
        return redirect(url_for('index'))

    # Initialize registration form
    form = DocRegForm()

    # Ensure data is validated on submit
    if request.method == 'POST' and form.validate():
        
        # Add doctor data to pending validations table
        new_doctor = DoctorPreVal(
            username = str(form.username.data).lower(),
            hash = generate_password_hash(form.password.data),
            full_name = form.full_name.data,
            gender = form.gender.data,
            dob = form.dob.data,
            email = form.email.data,
            contact = form.contact.data,
            reg_no = form.reg_no.data,
            specialities = form.specialities.data,
            created = datetime.now()
        )
        db.session.add(new_doctor)

        # Append a remark to Log
        append = Log(
            created = datetime.now(),
            user = DoctorPreVal.query.filter(DoctorPreVal.username == form.username.data).first().username,
            remarks = f"Doctor ({form.username.data}) data added to pending validations list"
        )
        db.session.add(append)

        # Commit all changes to database
        db.session.commit()
        
        # Flash a message and redirect to login page
        flash('Registration Successful!', "success")
        flash('Your details are being verified by administrators. Registration confirmation message will be sent to your email.', "info")
        return redirect(url_for('auth.login'))
    
    # Render the registration form
    return render_template('auth/doc_register.html', form = form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # Ensure user is not logged in
    if g.user is not None:
        return redirect(url_for('index'))

    # Initialize login form
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        # Clear flask session and add corresponding id of user into flask session
        flask_session.clear()
        pt = Patient.query.filter(Patient.username == form.username.data).first()
        doc = Doctor.query.filter(Doctor.username == form.username.data).first()
        admin = Admin.query.filter(Admin.username == form.username.data).first()
        if pt:
            flask_session['user_type'] = "patient"
            flask_session['user_id'] = pt.id
        elif doc:
            flask_session['user_type'] = "doctor"
            flask_session['user_id'] = doc.id
        elif admin:
            flask_session['user_type'] = "admin"
            flask_session['user_id'] = admin.id
        
        # Append a remark to log
        append = Log(
            created = datetime.now(),
            user = form.username.data,
            remarks = f"{flask_session.get('user_type').capitalize()} ({form.username.data}) logged in"
        )
        db.session.add(append)
        db.session.commit()
        
        
        flash('Login successful!', 'success')

        # Redirect admins to dashboard
        if admin:
            return redirect(url_for('admin.dash'))
        
        # Redirect other users to index
        return redirect(url_for('index'))
    
    return render_template('auth/login.html', form = form)


@bp.before_app_request
def load_logged_in_user():
    user_type = flask_session.get('user_type')
    user_id = flask_session.get('user_id')

    if user_id is None:
        g.user = None
    elif user_type == 'patient':
        g.user = Patient.query.filter(Patient.id == user_id).first()
    elif user_type == 'doctor':
        g.user = Doctor.query.filter(Doctor.id == user_id).first()
    elif user_type == 'admin':
        g.user = Admin.query.filter(Admin.id == user_id).first()


@bp.app_context_processor
def user_type_acp():
    return dict(user_type = flask_session.get('user_type'))


@bp.route('/logout')
@login_required
def logout():
    flask_session.clear()
    return redirect(url_for('index'))


""" This is used to add an admin into the database """
@bp.route('/register/41646d696e526567', methods=('GET', 'POST'))
# @admin_only
def admin_register():
    # Ensure data is validated on submit
    if request.method == 'POST':
        
        # Update database
        new_admin = Admin(
            username = request.form.get('username'),
            hash = generate_password_hash(request.form.get('password')),
            identification_no = request.form.get('id_no')
        )
        ## Add records to database and commit all changes
        db.session.add(new_admin)
        db.session.commit()
        
        # Flash a message and redirect to login page
        flash('Admin Added', "success")
        return redirect(url_for('auth.login'))
    
    # Render the registration form
    return render_template('auth/admin_register.html')
    