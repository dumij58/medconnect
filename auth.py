import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import RegistrationForm, LoginForm

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        full_name = form.full_name.data
        dob = form.dob.data
        email = form.email.data
        contact = form.contact.data
        password = form.password.data
        confirm = form.confirm.data
        # db = get_db()
        error = None

        print(form.username.data)
        print(form.username.errors)

        if form.validate_on_submit():
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.register'))

        if not username:
            error = "Username is required."
        elif not full_name:
            error = "Full name is required."
        elif not dob:
            error = "Date of birth is required."
        elif not email:
            error = "Email is required."
        elif not contact:
            error = "Contact is required."
        elif not password:
            error = "Password is required."
        elif not confirm:
            error = "Confirm your password."
        elif password != confirm:
            error = "Passwords doesn't match."

        flash(error)

    return render_template('auth/register.html', form = form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'

        elif not password:
            error = 'Password is required.'

        flash(error)

    return render_template('auth/login.html', form = form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
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