from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from markupsafe import escape
from datetime import datetime
from sqlalchemy import func

from .helpers import admin_only
from .models import db, DoctorPreVal, Doctor, Log, Hospital, Contact
from .forms import HlRegForm, ContactForm
from .email import send_email

bp = Blueprint('admin', __name__, url_prefix='/61646d696e')

@bp.route('/64617368')
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
        specializations = docdata.specializations,
        created = docdata.created,
        validated = datetime.now()
    )
    db.session.add(doc)
    
    # Send an email to user
    subject = "Welcome to MedConnect!"
    body = f"Greetings {docdata.username}, your registration has been validated. Now you can log into your account."
    send_email(docdata.email, subject, body)

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
    
    # Send an email to user
    subject = "Registration Rejected!"
    body = f"Sorry {docdata.username}, your registration has been rejected. Please check your details and re-register. If the details you entered are correct please send an email to dumij58.medconnect@gmail.com"
    send_email(docdata.email, subject, body)
    
    # Delete the temporarily stored doctor data
    db.session.delete(docdata)

    # Commit changes into the database
    db.session.commit()

    flash("Doctor registration rejected", 'info')
    return redirect(url_for('admin.dash'))


@bp.route('/686f73706974616c73', methods=('GET', 'POST'))
@admin_only
def hospitals():
    # Initialize form
    form = HlRegForm()
    showForm = False

    # Ensure data is validated on submit
    if request.method == 'POST':
        if form.validate():

            # Add records to database
            new_hospital = Hospital(
                name = form.name.data,
                email = form.email.data,
                contact = form.contact.data,
                address = form.address.data
            )
            db.session.add(new_hospital)

            # Append a remark to log
            append = Log(
                created = datetime.now(),
                user = g.user.username,
                remarks = f"Hospital ({form.name.data}) added to DB"
            )
            db.session.add(append)

            # Commit all changes to database
            db.session.commit()
            
            # Flash a message and redirect to login page
            showForm = False
            flash('Hospital Added!', "success")
    
        else:
            showForm = True

    hospitals = Hospital.query.all()
    return render_template('/admin/hospitals.html', show = showForm, form = form, hospitals = hospitals)


@bp.route('/686f73706974616c73/<int:hl_id>')
@admin_only
def hl_remove(hl_id):
    hospital = Hospital.query.filter(Hospital.id == escape(hl_id)).first()

    # Append a remark to log
    append = Log(
            created = datetime.now(),
            user = g.user.username,
            remarks = f"Admin ({g.user.username}) removed hospital ({hospital.name}) from datatbase"
        )
    db.session.add(append)

    flash(f'Hospital ({hospital.name}) removed!','info')
    
    # Delete the hospital data
    db.session.delete(hospital)

    # Commit changes into the database
    db.session.commit()

    ### todo: Send an email to hospital ###

    return redirect(url_for('admin.hospitals'))


@bp.route('/6d65737361676573')
@admin_only
def messages():
    form = ContactForm()
    messages = db.session.execute(db.select(Contact).where(Contact.status != "read")).scalars()
    msg_count = db.session.execute(db.select(func.count()).select_from(Contact).where(Contact.status != "read")).scalar()
    return render_template('/admin/messages.html', form = form, messages = messages, msg_count = msg_count)


@bp.route('/6d65737361676573/read_<int:id>')
@admin_only
def read_messages(id):
    db.session.execute(db.update(Contact).where(Contact.id == id).values(status = "read"))
    db.session.commit()
    flash("Message marked as read.", 'info')
    return redirect(url_for('admin.messages'))


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