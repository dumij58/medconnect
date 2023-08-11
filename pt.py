from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for, jsonify
)
from datetime import datetime, timedelta, date as d

from .helpers import login_required, f_datetime, get_total_apmts
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
    total_apmts = get_total_apmts(s_id)

    # Get the number of booked appointments
    apmts = db.session.execute(db.select(Appointment).where(Appointment.s_id == s_id)).all()
    if apmts:
        curr_apmts = len(apmts)
    else:
        curr_apmts = 0

    # Get the number of available appointments
    avail_apmts = total_apmts - curr_apmts

    # Calculate the approximate start time of the appointment (if each appointment is 20 minutes)
    apmt_duration = timedelta(minutes=20)
    apmt_start_dt = start_dt + (apmt_duration * curr_apmts)
    apmt_duration = int(apmt_duration.total_seconds() // 60)

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

        # Commit all changes to database
        db.session.commit()

        ### Send an email to user ###
        
        # Flash a message and redirect to login page
        flash('Booking Successful!', "success")
        return redirect(url_for('pt.apmts'))

    return render_template('pt/booking.html', session = session, avail_apmts = avail_apmts, start_dt = apmt_start_dt)


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