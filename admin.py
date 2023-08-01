from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from markupsafe import escape
from datetime import datetime

from .helpers import admin_only
from .models import db, DoctorPreVal, Doctor, Log

bp = Blueprint('admin', __name__, url_prefix='/61646d696e')

@bp.route('/64617368', methods=('GET', 'POST'))
@admin_only
def dash():
    docprevaldata = DoctorPreVal.query.all()
    log = Log.query.all()
    return render_template('admin/dash.html', rows = docprevaldata, log = log, log_len = len(log))

@bp.route('/76616c69646174650d0a/<int:doc_id>')
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

    # Append a remark to log
    append1 = Log(
            created = datetime.now(),
            user = Doctor.query.filter(Doctor.username == docdata.username).first().username,
            remarks = f"Doctor ({docdata.username}) added to DB"
        )
    db.session.add(append1)
    append2 = Log(
            created = datetime.now(),
            user = docdata.username,
            remarks = f"Admin ({g.user.username}) added doctor ({docdata.username}) to DB"
        )
    db.session.add(append2)

    # Delete the temporarily stored doctor data
    db.session.delete(docdata)

    # Commit changes into the database
    db.session.commit()
    
    ### todo: Send an email to doctor ###

    flash("Doctor added to the database", 'success')
    return redirect(url_for('admin.dash'))
    

@bp.route('/72656a6563740d0a/<int:doc_id>')
@admin_only
def doc_reject(doc_id):
    docdata = DoctorPreVal.query.filter(DoctorPreVal.id == escape(doc_id)).first()

    # Append a remark to log
    append = Log(
            created = datetime.now(),
            user = docdata.username,
            remarks = f"Admin ({g.user.username}) rejected doctor ({docdata.username}) registration"
        )
    db.session.add(append)
    
    # Delete the temporarily stored doctor data
    db.session.delete(docdata)

    # Commit changes into the database
    db.session.commit()

    ### todo: Send an email to doctor ###

    flash("Doctor registration rejected", 'info')
    return redirect(url_for('admin.dash'))


@bp.route('/6c6f67')
@admin_only
def log():
    log = Log.query.all()
    return render_template('/admin/log.html', log = log)


@bp.app_context_processor
def str_acp():
    def toString(s):
        return str(s)
    return dict(str = toString)