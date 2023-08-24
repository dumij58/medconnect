from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for, jsonify
)
from markupsafe import escape
from werkzeug.security import generate_password_hash
from datetime import datetime, date as d, timedelta

from .helpers import login_required, f_time, f_date, calc_total_apmts
from .models import db, Patient, Doctor, DoctorPreVal, Admin, Log, Hospital, DocSession, Appointment, VitalSign, ExaminationNote, OrderTest, TreatmentMedications, TreatmentOther, Medication, Referral, MedicalRecord
from .forms import SessionForm, PtRegForm, AddDetailsForm, ExaminationForm, OrderTestForm, DiagnosisTreatmentForm, FollowUpForm, ReferralForm

bp = Blueprint('doc', __name__, url_prefix='/doc')


@bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    apmts = db.session.execute(db.select(Appointment).join(Doctor).where(Doctor.id == g.user.id).where(Appointment.status != "no_show").where(Appointment.status != "ended").where(Appointment.datetime >= datetime.today()).where(Appointment.datetime <= datetime.today() + timedelta(days=1)).order_by(Appointment.datetime)).all()
    doc_sessions = db.session.execute(db.select(DocSession).where(DocSession.doc_id == g.user.id).where(DocSession.date >= d.today()).where(DocSession.date < d.today() + timedelta(days=7)).order_by(DocSession.date).order_by(DocSession.start_t)).all()
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

    doc_sessions = db.session.execute(db.select(DocSession).where(DocSession.doc_id == g.user.id).where(DocSession.date >= d.today()).order_by(DocSession.date).order_by(DocSession.start_t)).all()
    return render_template('doc/sessions.html', form = form, show = showForm, doc_sessions = doc_sessions)


@bp.route('/sessions/remove/<int:s_id>')
@login_required
def session_remove(s_id):
    doc_session = db.session.execute(db.select(DocSession).where(DocSession.id == escape(s_id))).first().DocSession

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
    return redirect(url_for('doc.doc_sessions'))


@bp.route('/sessions_panel/<int:s_id>')
@login_required
def session_panel(s_id):
    apmts = db.session.execute(db.select(Appointment).where(Appointment.s_id == s_id).where(Appointment.status != "no_show").where(Appointment.status != "ended")).all()
    return render_template('doc/session_panel.html', apmts = apmts)


@bp.route('/apmts', methods=('GET', 'POST'))
@login_required
def apmts():
    apmts = db.session.execute(db.select(Appointment).where(Doctor.id == g.user.id).where(Appointment.datetime >= datetime.now()).order_by(Appointment.datetime)).all()
    return render_template('doc/appointments.html', apmts = apmts)


@bp.route('/apmt/start/id=<int:id>')
@login_required
def apmt_start(id):
    apmt = db.session.execute(db.select(Appointment).where(Appointment.id == id)).scalar()

    # Update appointment status
    db.session.execute(db.update(Appointment).where(Appointment.id == id).values(status = "ongoing"))

    # Add new medical record
    new_medical_record = MedicalRecord(
        created = datetime.now(),
        doc_id = apmt.doc_id,
        pt_id = apmt.pt_id,
        hl_id = apmt.hl_id,
        apmt_id = id
    )
    db.session.add(new_medical_record)

    # Commit all changes to database
    db.session.commit()

    return redirect(url_for('doc.apmt_panel', id = id))


@bp.route('/apmt/no_show/id=<int:id>')
@login_required
def apmt_no_show(id):
    apmt = db.session.execute(db.select(Appointment).where(Appointment.id == id)).scalar()

    # Update appointment status
    db.session.execute(db.update(Appointment).where(Appointment.id == id).values(status = "no_show"))
    db.session.commit()

    return redirect(url_for('doc.session_panel', s_id = apmt.s_id))



@bp.route('/apmt_panel/id=<int:id>', methods=('GET', 'POST'))
@login_required
def apmt_panel(id):
    apmt = db.session.execute(db.select(Appointment).where(Appointment.id == id)).scalar()
    medical_record = db.session.execute(db.select(MedicalRecord).where(MedicalRecord.apmt_id == id)).scalar()

    if apmt:
        apmt = apmt
        if apmt.doc_id != g.user.id and flask_session.get('user_type') == 'doctor':
            return render_template('error.html', e_code = 401, e_text = "Unauthorized")
    else:
        return render_template('error.html', e_code = 404, e_text = "Not Found")
    
    if request.method == 'POST':
        # Get appointment data
        apmt_data = request.get_json()

        # Update appointment status
        db.session.execute(db.update(Appointment).where(Appointment.id == id).values(status = "ended"))
        
        # Update medical record and update follow up details if exists
        if "follow_up_date" in apmt_data:
            db.session.execute(db.update(MedicalRecord).where(MedicalRecord.id == medical_record.id).values(
                chief_complaint = apmt_data["chief_complaint"],
                diagnosis = apmt_data["diagnosis"],
                follow_up_date = datetime.strptime(apmt_data["follow_up_date"], '%Y-%m-%d').date(),
                follow_up_notes = apmt_data["follow_up_notes"]
            ))
        else:
            db.session.execute(db.update(MedicalRecord).where(MedicalRecord.id == medical_record.id).values(
                chief_complaint = apmt_data["chief_complaint"],
                diagnosis = apmt_data["diagnosis"]
            ))

        # Add referral form data if exists
        if "referral_reason" in apmt_data:
            if "doctor" in apmt_data:
                doc_id = db.session.execute(db.select(Doctor.id).where(Doctor.full_name == apmt_data["doctor"])).scalar()
                new_referral = Referral(
                    mr_id = medical_record.id,
                    date = d.today(),
                    doc_id = doc_id,
                    reason = apmt_data["referral_reason"]
                )
            else:
                new_referral = Referral(
                    mr_id = medical_record.id,
                    date = d.today(),
                    external_doc_name = apmt_data["ext_doctor_name"],
                    external_doc_specialization = apmt_data["ext_doctor_specialization"],
                    reason = apmt_data["referral_reason"]
                )
            db.session.add(new_referral)
                
        # Commit all changes to database
        db.session.commit()

        # flash message
        flash("Medical Record added to database","success")

        # Return a JSON response (Required, if not error-500)
        response = {
            'redirect_url': f"{url_for('doc.session_panel', s_id = apmt.s_id)}",
            'status': 'success'
        }
        return jsonify(response)

    else:
        # Initialize forms
        pt_info = PtRegForm()
        pt_details = AddDetailsForm()
        examination = ExaminationForm()
        order_test = OrderTestForm()
        diagnosis_treatment = DiagnosisTreatmentForm()
        follow_up = FollowUpForm()
        referral = ReferralForm()

        # Render template
        return render_template('doc/appointment_panel.html', apmt = apmt, medical_record = medical_record, form = pt_info, form2 = pt_details, form3 = examination, form4 = diagnosis_treatment, form5 = order_test, form6 = follow_up, form7 = referral)


@bp.route('/add_vital_sign/id=<int:mr_id>', methods=['POST'])
@login_required
def add_vital_sign(mr_id):
    # Get data from the POST request
    sign = request.json.get('sign')
    value = request.json.get('value')
    
    # Create a new Medication object and add it to the database
    new_vital_sign = VitalSign(
        mr_id = mr_id,
        sign = sign,
        value = value
    )
    db.session.add(new_vital_sign)
    db.session.commit()

    # Retrieve the updated data from the database
    vital_sign = db.session.execute(db.select(VitalSign).where(VitalSign.mr_id == mr_id).where(VitalSign.sign == sign).where(VitalSign.value == value)).scalar()
    
    # Render a template snippet with the new data
    row_html = render_template('doc/_vital_sign_row.html', vital_sign = vital_sign)

    return jsonify({'row_html': row_html})


@bp.route('/add_examination_note/id=<int:mr_id>', methods=['POST'])
@login_required
def add_examination_note(mr_id):
    # Get data from the POST request
    title = request.json.get('title')
    notes = request.json.get('notes')
    
    # Create a new Medication object and add it to the database
    new_examination_note = ExaminationNote(
        mr_id = mr_id,
        title = title,
        notes = notes
    )
    db.session.add(new_examination_note)
    db.session.commit()

    # Retrieve the updated data from the database
    examination_note = db.session.execute(db.select(ExaminationNote).where(ExaminationNote.mr_id == mr_id).where(ExaminationNote.title == title).where(ExaminationNote.notes == notes)).scalar()
    
    # Render a template snippet with the new data
    row_html = render_template('doc/_examination_note_row.html', examination_note = examination_note)

    return jsonify({'row_html': row_html})


@bp.route('/order_test/id=<int:mr_id>', methods=['POST'])
@login_required
def order_test(mr_id):
    # Get data from the POST request
    test_name = request.json.get('test_name')
    additional_notes = request.json.get('additional_notes')

    pt_id = db.session.execute(db.select(MedicalRecord.pt_id).where(MedicalRecord.id == mr_id)).scalar()
    
    # Create a new Medication object and add it to the database
    new_order_test = OrderTest(
        mr_id = mr_id,
        pt_id = pt_id,
        test_name = test_name,
        test_date = d.today(),
        additional_notes = additional_notes
    )
    db.session.add(new_order_test)
    db.session.commit()

    # Retrieve the updated data from the database
    order_test = db.session.execute(db.select(OrderTest).where(OrderTest.mr_id == mr_id).where(OrderTest.test_name == test_name)).scalar()
    
    # Render a template snippet with the new data
    row_html = render_template('doc/_order_test_row.html', order_test = order_test)

    return jsonify({'row_html': row_html})


@bp.route('/add_treatment/id=<int:mr_id>', methods=['POST'])
@login_required
def add_treatment(mr_id):
    # Get data from the POST request
    title = request.json.get('title')
    notes = request.json.get('treatment_notes')
    
    # Create a new Medication object and add it to the database
    new_treatment = TreatmentOther(
        mr_id = mr_id,
        title = title,
        notes = notes
    )
    db.session.add(new_treatment)
    db.session.commit()

    # Retrieve the updated data from the database
    treatment = db.session.execute(db.select(TreatmentOther).where(TreatmentOther.mr_id == mr_id).where(TreatmentOther.title == title).where(TreatmentOther.notes == notes)).scalar()
    
    # Render a template snippet with the new data
    row_html = render_template('doc/_treatment_row.html', treatment = treatment)

    return jsonify({'row_html': row_html})


@bp.route('/add_medication/id=<int:mr_id>', methods=['POST'])
@login_required
def add_medication(mr_id):
    # Get data from the POST request
    medication_name = request.json.get('medication_name')
    dosage = request.json.get('dosage')
    frequency = request.json.get('frequency')
    pt_full_name = request.json.get('pt_full_name')
    start_date = datetime.today()

    pt_id = db.session.execute(db.select(Patient.id).where(Patient.full_name == pt_full_name)).scalar()

    # Create a new Medication object and add it to the database
    new_medication = Medication(
        pt_id = pt_id,
        medication_name = medication_name,
        dosage = dosage,
        frequency = frequency,
        start_date = start_date
    )
    db.session.add(new_medication)

    new_treatment_medication = TreatmentMedications(
        mr_id = mr_id,
        medication_name = medication_name,
        dosage = dosage,
        frequency = frequency,
        start_date = start_date
    )
    db.session.add(new_treatment_medication)

    db.session.commit()

    # Retrieve the updated data from the database
    medication = db.session.execute(db.select(TreatmentMedications).where(TreatmentMedications.mr_id == mr_id).where(TreatmentMedications.medication_name == medication_name)).scalar()
    
    # Render a template snippet with the new data
    row_html = render_template('doc/_medication_row.html', medication = medication)

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
    specializations = form_data['specializations']

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
    if specializations and specializations != doc.specializations:
        db.session.execute(updateStatement.values(specializations = specializations))
        updatedValues["specializations"] = specializations
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


""" Get the Doctor list into the search form through js """
@bp.route('/referral_get_doc')
@login_required
def referral_get_doc():
    doctors = db.session.execute(db.select(Doctor)).scalars()
    doctor_names = [f"Dr. {doctor.full_name}" for doctor in doctors]
    return jsonify(doctor_names)

""" Get the Patient list into the search form through js """
@bp.route('/get_pt_list')
@login_required
def get_pt_list():
    patients = db.session.execute(db.select(Patient)).scalars()
    Patient_names = [patient.full_name for patient in patients]
    return jsonify(Patient_names)