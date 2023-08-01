from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from markupsafe import escape
from datetime import datetime

from .helpers import login_required, admin_only
from .models import db, DoctorPreVal, Doctor

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('main/index.html')

@bp.route('/61646d696e', methods=('GET', 'POST'))
@login_required
@admin_only
def admin_dash():
    docprevaldata = DoctorPreVal.query.all()
    return render_template('main/admin_dash.html', rows = docprevaldata)

@bp.route('/61646d696e/76616c69646174650d0a/<int:doc_id>')
@login_required
@admin_only
def doc_validate(doc_id):
    docdata = DoctorPreVal.query.filter(DoctorPreVal.id == escape(doc_id)).first()

    # Insert the doctor data into the database
    doc = Doctor(
        username = docdata.username,
        hash = docdata.hash,
        full_name = docdata.full_name,
        gender = docdata.gender,
        dob = docdata.dob,
        email = docdata.email,
        contact = docdata.contact,
        reg_no = docdata.reg_no,
        specialities = docdata.specialities,
        created = docdata.created,
        validated = datetime.now()
    )
    db.session.add(doc)

    # Delete the temporarily stored doctor data
    db.session.delete(docdata)

    # Commit changes into the database
    db.session.commit()
    
    ### todo: Send an email to doctor ###

    flash("Doctor added to the database", 'success')
    return redirect(url_for('main.admin_dash'))
    

@bp.route('/61646d696e/72656a6563740d0a/<int:doc_id>')
@login_required
@admin_only
def doc_reject(doc_id):
    docdata = DoctorPreVal.query.filter(DoctorPreVal.id == escape(doc_id)).first()
    
    # Delete the temporarily stored doctor data
    db.session.delete(docdata)

    # Commit changes into the database
    db.session.commit()

    ### todo: Send an email to doctor ###

    flash("Doctor registration rejected", 'info')
    return redirect(url_for('main.admin_dash'))


@bp.app_context_processor
def str_acp():
    def toString(s):
        return str(s)
    return dict(str = toString)