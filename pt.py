from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for, jsonify
)
from datetime import datetime, timedelta, date as d

from .helpers import login_required, f_datetime
from .models import db, Patient, Doctor, Log, Hospital, DocSession, Appointment, Medication, Surgery, Vaccination, FamilyHistory, MedicalHistory
from .forms import AddDetailsForm

bp = Blueprint('pt', __name__, url_prefix='/pt')


@bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    user = db.session.execute(db.select(Patient).where(Patient.id == g.user.id)).first().Patient
    apmts = db.session.execute(db.select(Appointment, Doctor, Hospital).join(Doctor, Appointment.doc_id == Doctor.id).join(Patient, Appointment.pt_id == Patient.id).join(Hospital, Appointment.hl_id == Hospital.id).where(Patient.id == g.user.id).where(Appointment.datetime >= datetime.now()).order_by(Appointment.datetime)).all()
    return render_template('pt/dash.html', check_details = user.details_added, apmts = apmts)

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


@bp.route('/add_details', methods=('GET', 'POST'))
@login_required
def add_details():
    # Initialize registration form
    form = AddDetailsForm()

    # Ensure data is validated on submit
    if request.method == 'POST':
        # Change detail_added in patient table to True
        db.session.execute(db.update(Patient).where(Patient.id == g.user.id).values(details_added = True))
        db.session.commit()

        # Flash a message and redirect to login page
        # return redirect(url_for('pt.profile'))
        return redirect(url_for('pt.dash'))
    
    medications = db.session.execute(db.select(Medication).where(Medication.pt_id == g.user.id)).all()
    surgeries = db.session.execute(db.select(Surgery).where(Surgery.pt_id == g.user.id)).all()
    vaccinations = db.session.execute(db.select(Vaccination).where(Vaccination.pt_id == g.user.id)).all()
    fh_rows = db.session.execute(db.select(FamilyHistory).where(FamilyHistory.pt_id == g.user.id)).all()
    mh_rows = db.session.execute(db.select(MedicalHistory).where(MedicalHistory.pt_id == g.user.id)).all()

    # Render the registration form
    return render_template('pt/add_details.html',form = form, medications = medications, surgeries = surgeries, vaccinations = vaccinations, fh_rows = fh_rows, mh_rows = mh_rows)


@bp.route('/add_details/remove', methods=['POST'])
@login_required
def add_details_remove():
    id = request.json.get('id')
    type = request.json.get('type')

    # Get the entry to be removed using type and id
    if type == 'medical-history':
        db.session.execute(db.delete(MedicalHistory).where(MedicalHistory.id == id))
    elif type == 'medication':
        db.session.execute(db.delete(Medication).where(Medication.id == id))
    elif type == 'surgery':
        db.session.execute(db.delete(Surgery).where(Surgery.id == id))
    elif type == 'vaccination':
        db.session.execute(db.delete(Vaccination).where(Vaccination.id == id))
    elif type == 'family-history':
        db.session.execute(db.delete(FamilyHistory).where(FamilyHistory.id == id))

    # Commit all changes
    db.session.commit()
    
    # Return a JSON response (Required, if not error-500)
    response = {
        'message': 'Entry removed successfully.',
        'status': 'success'
    }
    return jsonify(response)



@bp.route('/add_medical_history', methods=['POST'])
@login_required
def add_medical_history():
    # Get data from the POST request
    medical_condition = request.json.get('medical_condition')
    diagnosis_date = datetime.strptime(request.json.get('diagnosis_date'), '%Y-%m-%d').date()
    treatment = request.json.get('treatment')
    
    # Create a new Medication object and add it to the database
    new_medical_history = MedicalHistory(
        pt_id = g.user.id,
        medical_condition = medical_condition,
        diagnosis_date = diagnosis_date,
        treatment = treatment
    )
    db.session.add(new_medical_history)
    db.session.commit()

    # Retrieve the updated data from the database
    mh_row = db.session.execute(db.select(MedicalHistory).where(MedicalHistory.pt_id == g.user.id).where(MedicalHistory.medical_condition == medical_condition).where(MedicalHistory.diagnosis_date == diagnosis_date).where(MedicalHistory.treatment == treatment)).first().MedicalHistory
    
    # Render a template snippet with the new data
    row_html = render_template('pt/_medical_history_row.html', mh_row = mh_row)

    return jsonify({'row_html': row_html})


@bp.route('/add_medication', methods=['POST'])
@login_required
def add_medication():
    # Get data from the POST request
    medication_name = request.json.get('medication_name')
    dosage = request.json.get('dosage')
    frequency = request.json.get('frequency')
    start_date = datetime.strptime(request.json.get('start_date'), '%Y-%m-%d').date()

    # Create a new Medication object and add it to the database
    new_medication = Medication(
        pt_id = g.user.id,
        medication_name = medication_name,
        dosage = dosage,
        frequency = frequency,
        start_date = start_date
    )
    db.session.add(new_medication)
    db.session.commit()

    # Retrieve the updated data from the database
    medication = db.session.execute(db.select(Medication).where(Medication.pt_id == g.user.id).where(Medication.medication_name == medication_name)).first().Medication
    
    # Render a template snippet with the new data
    row_html = render_template('pt/_medication_row.html', medication = medication)

    return jsonify({'row_html': row_html})


@bp.route('/add_surgery', methods=['POST'])
@login_required
def add_surgery():
    # Get data from the POST request
    surgery_name = request.json.get('surgery_name')
    date = datetime.strptime(request.json.get('date'), '%Y-%m-%d').date()
    notes = request.json.get('notes')
    
    # Create a new Medication object and add it to the database
    new_surgery = Surgery(
        pt_id = g.user.id,
        surgery_name = surgery_name,
        date = date,
        notes = notes
    )
    db.session.add(new_surgery)
    db.session.commit()

    # Retrieve the updated data from the database
    surgery = db.session.execute(db.select(Surgery).where(Surgery.pt_id == g.user.id).where(Surgery.surgery_name == surgery_name).where(Surgery.date == date)).first().Surgery
    
    # Render a template snippet with the new data
    row_html = render_template('pt/_surgery_row.html', surgery = surgery)

    return jsonify({'row_html': row_html})


@bp.route('/add_vaccination', methods=['POST'])
@login_required
def add_vaccination():
    # Get data from the POST request
    vaccine_name = request.json.get('vaccine_name')
    administration_date = datetime.strptime(request.json.get('administration_date'), '%Y-%m-%d').date()
    notes = request.json.get('notes')
    
    # Create a new Medication object and add it to the database
    new_vaccination = Vaccination(
        pt_id = g.user.id,
        vaccine_name = vaccine_name,
        administration_date = administration_date,
        notes = notes
    )
    db.session.add(new_vaccination)
    db.session.commit()

    # Retrieve the updated data from the database
    vaccination = db.session.execute(db.select(Vaccination).where(Vaccination.pt_id == g.user.id).where(Vaccination.vaccine_name == vaccine_name).where(Vaccination.administration_date == administration_date)).first().Vaccination
    
    # Render a template snippet with the new data
    row_html = render_template('pt/_vaccination_row.html', vaccination = vaccination)

    return jsonify({'row_html': row_html})


@bp.route('/add_family_history', methods=['POST'])
@login_required
def add_family_history():
    # Get data from the POST request
    relationship = request.json.get('relationship')
    medical_condition = request.json.get('medical_condition')
    
    # Create a new Medication object and add it to the database
    new_family_history = FamilyHistory(
        pt_id = g.user.id,
        relationship = relationship,
        medical_condition = medical_condition
    )
    db.session.add(new_family_history)
    db.session.commit()

    # Retrieve the updated data from the database
    fh_row = db.session.execute(db.select(FamilyHistory).where(FamilyHistory.pt_id == g.user.id).where(FamilyHistory.relationship == relationship).where(FamilyHistory.medical_condition == medical_condition)).first().FamilyHistory
    
    # Render a template snippet with the new data
    row_html = render_template('pt/_family_history_row.html', fh_row = fh_row)

    return jsonify({'row_html': row_html})


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