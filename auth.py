import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import RegistrationForm, LoginForm

from medconnect.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # if error is None:
        #    try:
        #        db.execute(
        #            "INSERT INTO user (username, password) VALUES (?, ?)",
        #            (username, generate_password_hash(password)),
        #        )
        #        db.commit()
        #    except db.IntegrityError:
        #        error = f"User {username} is already registered."
        #    else:
        #        return redirect(url_for("auth.login"))

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
