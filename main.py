from flask import (
    Blueprint, g, flash, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from markupsafe import escape
from datetime import datetime

from .helpers import login_required, admin_only
from .models import db, Medication, Surgery, Vaccination, FamilyHistory, MedicalHistory, Appointment
from .forms import DocRegForm, PtRegForm, AddDetailsForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/profile/<user_type>_id=<int:id>')
@login_required
def profile(user_type, id):
    pt_form = PtRegForm()
    doc_form = DocRegForm()
    pt_details = AddDetailsForm()

    # Ensure only user has access to edit data in his profile
    if user_type != session.get('user_type') or id != g.user.id:
        return render_template('error.html', e_code = 401, e_text = "Unauthorized")

    if user_type == 'doctor':
        return render_template('doc/profile.html', form = doc_form)
    
    elif user_type == 'patient':
        mh_rows = db.session.execute(db.select(MedicalHistory).where(MedicalHistory.pt_id == g.user.id)).all()
        medications = db.session.execute(db.select(Medication).where(Medication.pt_id == g.user.id)).all()
        surgeries = db.session.execute(db.select(Surgery).where(Surgery.pt_id == g.user.id)).all()
        vaccinations = db.session.execute(db.select(Vaccination).where(Vaccination.pt_id == g.user.id)).all()
        fh_rows = db.session.execute(db.select(FamilyHistory).where(FamilyHistory.pt_id == g.user.id)).all()
        return render_template('pt/profile.html', form = pt_form, form2 = pt_details, mh_rows = mh_rows, medications = medications, surgeries = surgeries, vaccinations = vaccinations, fh_rows = fh_rows)
    
    elif user_type == 'admin':
        return render_template('admin/profile.html')
    