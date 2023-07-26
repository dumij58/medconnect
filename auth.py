import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone

from .models import db, Patient
from .forms import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # Initialize registration form, database and variables
    form = RegistrationForm()

    # Ensure data is validated on submit
    if request.method == 'POST' and form.validate():

        # Post validate user input (Validation code is in forms.py)
        uname = form.username.data
        uname = str(uname).lower()
        email = form.email.data
        ## Check if user exist
        if Patient.query.filter(Patient.username == uname).first():
            flash(f"User {uname} already exist.", "danger")
            return redirect(url_for('auth.register'))
        if Patient.query.filter(Patient.email == email).first():
            flash(f"User with email ({email}) already exist.", "danger")
            return redirect(url_for('auth.register'))
        
        # Update database
        new_patient = Patient(
            username = uname,
            full_name = form.full_name.data,
            dob = form.dob.data,
            email = email,
            contact = form.contact.data,
            hash = generate_password_hash(form.password.data),
            created = datetime.now()
        )
        ## Add records to database and commit all changes
        db.session.add(new_patient)
        db.session.commit()
        
        # Flash a message and redirect to login page
        flash('Registration Successful!', "success")
        return redirect(url_for('auth.login'))
    
    else:
        # Render the registration form
        return render_template('auth/register.html', form = form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        flash('Login successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form = form)

"""
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = g.db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
    """