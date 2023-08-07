from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for
)
from werkzeug.security import generate_password_hash

from .helpers import login_required
from .models import db, Patient, Doctor, DoctorPreVal, Admin, Log

bp = Blueprint('doc', __name__, url_prefix='/doc')


@bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    return render_template('doc/dash.html')