import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # Initialize registration form, database and variables
    form = RegistrationForm()
    db = g.db
    uname = form.username.data
    full_name = form.full_name.data
    dob = form.dob.data
    email = form.email.data
    contact = form.contact.data

    # Ensure data is validated on submit
    if request.method == 'POST' and form.validate():

        print(db.execute('SELECT id FROM patient WHERE username = ?', (uname,)))
            #flash(f'User {uname} already exist.', 'danger')

        # Update database
        try:
            #print(f"{uname}, {full_name}, {dob}, {email}, {contact}, {generate_password_hash(form.password.data)}")
            db.execute(
                'INSERT INTO patient (username, full_name, dob, email, contact, hash) VALUES (?, ?, ?, ?, ?, ?)', 
                (uname, full_name, dob, email, contact, generate_password_hash(form.password.data))
            )
            #db.commit()
            print("Database Updated!")
        except db.Error as er:
            print("Updating database failed!")
            #print('SQLite error: %s' % (' '.join(er.args)))
            #print("Exception class is: ", er.__class__)
            flash('Registration failed! Please contact support', 'danger')
            return redirect(url_for('auth.register'))

        # Flash a message and redirect to login page
        flash('Registration successful!')
        return redirect(url_for('auth.login'))
    
    else:
        # Render the registration form
        flash('Create your MedConnect account here!', 'success')
        return render_template('auth/register.html', form = form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        flash('Login successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form = form)


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