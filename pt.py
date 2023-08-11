from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for, jsonify
)
from datetime import datetime, timedelta, date as d

from .helpers import login_required, f_datetime
from .models import db, Patient, Doctor, DoctorPreVal, Admin, Log, Hospital, DocSession, Appointment

bp = Blueprint('pt', __name__, url_prefix='/pt')


@bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    apmts = db.session.execute(db.select(Appointment, Doctor, Hospital).join(Doctor, Appointment.doc_id == Doctor.id).join(Patient, Appointment.pt_id == Patient.id).join(Hospital, Appointment.hl_id == Hospital.id).where(Patient.id == g.user.id).where(Appointment.datetime >= datetime.now()).order_by(Appointment.datetime)).all()
    return render_template('pt/dash.html', apmts = apmts)

@bp.route('/apmts')
@login_required
def apmts():
    # Get doctor name, hospital name and date from url args, and get doctor id and hospital id from database
    doc_id = db.session.execute(db.select(Doctor.id).where(Doctor.full_name == str(request.args.get('doc'))[4:])).scalar()
    hl_id  = db.session.execute(db.select(Hospital.id).where(Hospital.name == request.args.get('hl'))).scalar()
    date  = request.args.get('date')

    # Join statement for joining doc_session, doctor and hospital tables
    joined = db.select(DocSession, Doctor, Hospital).join(Doctor).join(Hospital)

    # Ensure every possibility of user input gets a result
    if doc_id and hl_id and date:
        sessions = db.session.execute(joined.where(Doctor.id == doc_id).where(Hospital.id == hl_id).where(DocSession.date == date).where(DocSession.date > d.today()).order_by(DocSession.start_t))
    elif doc_id and hl_id:
        sessions = db.session.execute(joined.where(Doctor.id == doc_id).where(Hospital.id == hl_id).where(DocSession.date > d.today()).order_by(DocSession.date).order_by(DocSession.start_t))
    elif doc_id and date:
        sessions = db.session.execute(joined.where(Doctor.id == doc_id).where(DocSession.date == date).where(DocSession.date > d.today()).order_by(Hospital.name).order_by(DocSession.start_t))
    elif date and hl_id:
        sessions = db.session.execute(joined.where(Hospital.id == hl_id).where(DocSession.date == date).where(DocSession.date > d.today()).order_by(Doctor.full_name).order_by(DocSession.start_t))
    elif doc_id:
        sessions = db.session.execute(joined.where(Doctor.id == doc_id).where(DocSession.date > d.today()).order_by(Hospital.name).order_by(DocSession.date).order_by(DocSession.start_t))
    elif hl_id:
        sessions = db.session.execute(joined.where(Hospital.id == hl_id).where(DocSession.date > d.today()).order_by(Doctor.full_name).order_by(DocSession.date).order_by(DocSession.start_t))
    else:
        sessions = None

    return render_template('pt/appointments.html', sessions = sessions)


@bp.route('/apmts/book/<int:s_id>', methods=('GET', 'POST'))
@login_required
def book_apmt(s_id):
    session = db.session.execute(db.select(DocSession, Doctor, Hospital).join(Doctor).join(Hospital).where(DocSession.id == s_id)).first()
    start_dt = datetime.combine(session.DocSession.date, session.DocSession.start_t)
    total_apmts = session.DocSession.total_apmts

    # Calculate the approximate start time of the appointment (if each appointment is 20 minutes)
    apmt_duration = timedelta(minutes=20)
    apmt_start_dt = start_dt + (apmt_duration * session.DocSession.apmt_count)

    if request.method == 'POST':

        # Update database
        new_apmt = Appointment(
            datetime = apmt_start_dt,
            doc_id = session.Doctor.id,
            pt_id = g.user.id,
            hl_id = session.Hospital.id,
            s_id = session.DocSession.id
        )
        ## Add records to database and commit all changes
        db.session.add(new_apmt)

        # Append a remark to log
        append = Log(
            created = datetime.now(),
            user = g.user.username,
            remarks = f"{g.user.username} booked an appointment (Session ID-{session.DocSession.id}) on {f_datetime(apmt_start_dt)}"
        )
        db.session.add(append)

        # Update apmt_count in session
        db.session.execute(db.update(DocSession).where(DocSession.id == s_id).values(apmt_count = session.DocSession.apmt_count + 1))

        # Commit all changes to database
        db.session.commit()

        ### Send an email to user ###
        
        # Flash a message and redirect to login page
        flash('Booking Successful!', "success")
        return redirect(url_for('pt.apmts'))
    
    no_cancel = False
    if session.DocSession.date < timedelta(days=7) + d.today():
        no_cancel = True
    return render_template('pt/booking.html', session = session, start_dt = apmt_start_dt, no_cancel = no_cancel)


@bp.route('/apmts/cancel/<int:id>')
@login_required
def cancel_apmt(id):
    apmt = db.session.execute(db.select(Appointment, DocSession, Doctor).join(DocSession, Appointment.s_id == DocSession.id).join(Doctor, Appointment.doc_id == Doctor.id).where(Appointment.id == id)).first()

    # Update apmt_count in session
    db.session.execute(db.update(DocSession).where(DocSession.id == apmt.Appointment.s_id).values(apmt_count = apmt.DocSession.apmt_count - 1))

    # Append a remark to log
    append = Log(
        created = datetime.now(),
        user = g.user.username,
        remarks = f"{g.user.username} cancelled the appointment ({f_datetime(apmt.Appointment.datetime)}) with doctor ({apmt.Doctor.username})"
    )
    db.session.add(append)

    # Delete appointment from database
    db.session.execute(db.delete(Appointment).where(Appointment.id == id))

    # Commit all changes to database
    db.session.commit()

    return redirect(url_for('pt.dash'))


""" Get the Doctor list into the search form through js """
@bp.route('/apmts/get_doc')
@login_required
def get_doc():
    doctors = Doctor.query.all()
    doctor_names = [f"Dr. {doctor.full_name}" for doctor in doctors]
    return jsonify(doctor_names)


""" Get the Hospital list into the search form through js """
@bp.route('/apmts/get_hl')
@login_required
def get_hl():
    hospitals = Hospital.query.all()
    hospital_names = [hospital.name for hospital in hospitals]
    return jsonify(hospital_names)


@bp.context_processor
def utility_processor():
    def no_cancel(dt):
        if dt < timedelta(days=7) + datetime.now():
            return True
        else:
            return False
    return dict(no_cancel=no_cancel)