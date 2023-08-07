from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for
)
from werkzeug.security import generate_password_hash

from .helpers import login_required
from .models import db, Patient, Doctor, DoctorPreVal, Admin, Log, Hospital
from .forms import SessionForm

bp = Blueprint('doc', __name__, url_prefix='/doc')


@bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    return render_template('doc/dash.html')

@bp.route('/sessions', methods=('GET', 'POST'))
@login_required
def sessions():
    form = SessionForm()
    form.hl_id.choices = [ (hl.id, hl.name) for hl in Hospital.query.order_by('name') ]
    print(Hospital.query.order_by('name'))
    return render_template('doc/sessions.html', form = form)

@bp.route('/sessions/add', methods=('GET', 'POST'))
@login_required
def add_session():
    flash('Session Added', 'success')
    return redirect(url_for('doc.sessions'))