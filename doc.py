from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for, jsonify
)
from markupsafe import escape
from werkzeug.security import generate_password_hash
from datetime import datetime, date as d, timedelta

from .helpers import login_required, f_time, f_date, calc_total_apmts
from .models import db, Patient, Doctor, DoctorPreVal, Admin, Log, Hospital, DocSession, Appointment, Specialization
from .forms import SessionForm, AddSpecializationForm

bp = Blueprint('doc', __name__, url_prefix='/doc')


@bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    apmts = db.session.execute(db.select(Appointment, Patient, Hospital).join(Doctor, Appointment.doc_id == Doctor.id).join(Patient, Appointment.pt_id == Patient.id).join(Hospital, Appointment.hl_id == Hospital.id).where(Doctor.id == g.user.id).where(Appointment.datetime >= datetime.now()).order_by(Appointment.datetime)).all()
    doc_sessions = db.session.execute(db.select(DocSession, Doctor, Hospital).join(Doctor).join(Hospital).where(DocSession.doc_id == g.user.id).where(DocSession.date >= d.today()).where(DocSession.date < d.today() + timedelta(days=7)).order_by(DocSession.date).order_by(DocSession.start_t)).all()
    return render_template('doc/dash.html', doc_sessions = doc_sessions, apmts = apmts)

@bp.route('/sessions', methods=('GET', 'POST'))
@login_required
def doc_sessions():
    form = SessionForm()
    form.hl_id.choices = [ (hl.id, hl.name) for hl in Hospital.query.order_by('name') ]

    # Declare variables
    showForm = False
    date = form.date.data
    start_t = form.start_t.data
    end_t = form.end_t.data

    # Ensure data is validated on submit
    if request.method == 'POST':

        if form.validate():

            # Get total appointments for the duration of this session
            total_apmts = calc_total_apmts(date, start_t, end_t)
            
            # Add records to database
            new_doc_session = DocSession(
                hl_id = form.hl_id.data,
                doc_id = g.user.id,
                date = date,
                start_t = start_t,
                end_t = end_t,
                total_apmts = total_apmts
                # Don't need to add "apmt_count" it has a default value of 0
            )
            db.session.add(new_doc_session)

            # Append a remark to log
            append = Log(
                created = datetime.now(),
                user = g.user.username,
                remarks = f"Session (On {f_date(form.date.data)} from {f_time(form.start_t.data)} to {f_time(form.end_t.data)}) added to Doctor ({g.user.username})"
            )
            db.session.add(append)

            # Commit all changes to database
            db.session.commit()
            
            # Flash a message and redirect to login page
            showForm = False
            flash('Session Added!', "success")
    
        else:
            showForm = True

    #doc_sessions = db.session.execute(db.select(DocSession, Hospital).join(Hospital).where(DocSession.date >= d.today()).order_by(DocSession.date, DocSession.start_t))
    doc_sessions = db.session.execute(db.select(DocSession, Doctor, Hospital).join(Doctor).join(Hospital).where(DocSession.doc_id == g.user.id).where(DocSession.date >= d.today()).order_by(DocSession.date).order_by(DocSession.start_t)).all()
    return render_template('doc/sessions.html', form = form, show = showForm, doc_sessions = doc_sessions)


@bp.route('/sessions/remove/<int:s_id>')
@login_required
def session_remove(s_id):
    doc_session = DocSession.query.filter(DocSession.id == escape(s_id)).first() ### Update Legacy commands

    # Append a remark to log
    append = Log(
            created = datetime.now(),
            user = g.user.username,
            remarks = f"Session (On {f_date(doc_session.date)} from {f_time(doc_session.start_t)} to {f_time(doc_session.end_t)}) removed from Doctor ({g.user.username})"
        )
    db.session.add(append)
    
    # Delete the hospital data
    db.session.delete(doc_session)

    # Commit changes into the database
    db.session.commit()

    flash(f'Session removed!','info')
    return redirect(url_for('doc.sessions'))


@bp.route('/apmts', methods=('GET', 'POST'))
@login_required
def apmts():
    apmts = db.session.execute(db.select(Appointment, Patient, Hospital).join(Doctor, Appointment.doc_id == Doctor.id).join(Patient, Appointment.pt_id == Patient.id).join(Hospital, Appointment.hl_id == Hospital.id).where(Doctor.id == g.user.id).where(Appointment.datetime >= datetime.now()).order_by(Appointment.datetime)).all()
    print(apmts)
    return render_template('doc/appointments.html', apmts = apmts)


@bp.route('/add_specialization', methods=['POST'])
@login_required
def add_specialization():
    # Get data from the POST request
    specialization = request.json.get('specialization')
    
    # Create a new Medication object and add it to the database
    new_specialization = Specialization(
        doc_id = g.user.id,
        specialization = specialization,
    )
    db.session.add(new_specialization)
    db.session.commit()

    # Retrieve the updated data from the database
    specialization = db.session.execute(db.select(Specialization).where(Specialization.doc_id == g.user.id).where(Specialization.specialization == specialization)).first().Specialization
    
    # Render a template snippet with the new data
    row_html = render_template('doc/_specialization_row.html', specialization = specialization)

    return jsonify({'row_html': row_html})


@bp.route('/change_details', methods=['POST'])
@login_required
def change_details():
    form_data = request.get_json()
    full_name = form_data['full_name']
    gender = form_data['gender']
    dob = datetime.strptime(form_data['dob'], '%Y-%m-%d').date()
    email = form_data['email']
    contact = form_data['contact']

    doc = db.session.execute(db.select(Doctor).where(Doctor.id == g.user.id)).first().Doctor
    updateStatement = db.update(Doctor).where(Doctor.id == g.user.id)
    updatedValues = {}

    if full_name and full_name != doc.full_name:
        db.session.execute(updateStatement.values(full_name = full_name))
        updatedValues["full_name"] = full_name
    if gender and gender != doc.gender:
        db.session.execute(updateStatement.values(gender = gender))
        updatedValues["gender"] = gender
    if dob and dob != doc.dob:
        db.session.execute(updateStatement.values(dob = dob))
        updatedValues["dob"] = dob.strftime('%Y-%m-%d')
    if email and email != doc.email:
        db.session.execute(updateStatement.values(email = email))
        updatedValues["email"] = email
    if contact and contact != doc.contact:
        db.session.execute(updateStatement.values(contact = contact))
        updatedValues["contact"] = contact
    db.session.commit()
    
    return jsonify(updatedValues)


@bp.route('/change_uname', methods=['POST'])
@login_required
def change_uname():
    uname = str(request.json.get('username')).lower()
    user = db.session.execute(db.select(Doctor).where(Doctor.username == uname)).first()
    response = {}

    if db.session.execute(db.select(Patient).where(Patient.username == uname)).first() or \
        db.session.execute(db.select(Doctor).where(Doctor.username == uname)).first() or \
        db.session.execute(db.select(Admin).where(Admin.username == uname)).first():
        response['message'] = 'username taken' 
        return jsonify(response)

    db.session.execute(db.update(Doctor).where(Doctor.id == g.user.id).values(username = uname))
    db.session.commit()
    response['username'] = uname
    response['message'] = 'success'
    return jsonify(response)

@bp.route('/add_specialization/remove', methods=['POST'])
@login_required
def add_specialization_remove():
    id = request.json.get('id')

    # Get the entry to be removed using type and id
    db.session.execute(db.delete(Specialization).where(Specialization.id == id))

    # Commit all changes
    db.session.commit()
    
    # Return a JSON response (Required, if not error-500)
    response = {
        'message': 'Entry removed successfully.',
        'status': 'success'
    }
    return jsonify(response)