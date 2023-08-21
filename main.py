from flask import (
    Blueprint, g, flash, redirect, render_template, request, url_for, session as flask_session
)
from werkzeug.exceptions import abort
from markupsafe import escape
from datetime import datetime, timedelta

from .helpers import login_required, admin_only
from .models import db, Medication, Surgery, Vaccination, FamilyHistory, MedicalHistory, Doctor, Patient, Hospital, MedicalRecord
from .forms import DocRegForm, PtRegForm, AddDetailsForm, ExaminationForm, DiagnosisTreatmentForm

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
    if user_type != flask_session.get('user_type') or id != g.user.id:
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

@bp.route('/search/medical_records')
@login_required
def mr_search():
    # Get doctor name, hospital name and date from url args, and get doctor id and hospital id from database
    doc_id = db.session.execute(db.select(Doctor.id).where(Doctor.full_name == str(request.args.get('doc'))[4:])).scalar()
    pt_id = db.session.execute(db.select(Patient.id).where(Patient.full_name == request.args.get('pt'))).scalar()
    hl_id  = db.session.execute(db.select(Hospital.id).where(Hospital.name == request.args.get('hl'))).scalar()
    date  = request.args.get('date')

    print(pt_id)

    records = None
    joinedStatement = db.select(MedicalRecord, Doctor, Patient, Hospital).join(Doctor, MedicalRecord.doc_id == Doctor.id).join(Patient, MedicalRecord.pt_id == Patient.id).join(Hospital, MedicalRecord.hl_id == Hospital.id)

    # Ensure every possibility of user input gets a result
    u_type = flask_session.get('user_type')

    if not doc_id and not pt_id and hl_id:
        print("hl")
        records = db.session.execute(joinedStatement.where(Hospital.id == hl_id).order_by(Doctor.full_name).order_by(MedicalRecord.created)).scalars()

        if date:
            print("hl, date")
            dt = datetime.strptime(date, '%Y-%m-%d')
            records = db.session.execute(joinedStatement.where(Hospital.id == hl_id).where(MedicalRecord.created > dt).where(MedicalRecord.created < dt + timedelta(days=1)).order_by(Doctor.full_name)).scalars()
        
    elif u_type == 'patient':
        if doc_id:
            print("doc")
            records = db.session.execute(joinedStatement.where(Doctor.id == doc_id).order_by(Hospital.name).order_by(MedicalRecord.created)).scalars()

            if date:
                print("doc, date")
                dt = datetime.strptime(date, '%Y-%m-%d')
                records = db.session.execute(joinedStatement.where(Hospital.id == hl_id).where(MedicalRecord.created > dt).where(MedicalRecord.created < dt + timedelta(days=1)).order_by(Doctor.full_name)).scalars()

            if hl_id:
                print("doc, hl")
                records = db.session.execute(joinedStatement.where(Doctor.id == doc_id).where(Hospital.id == hl_id).order_by(MedicalRecord.created)).scalars()

                if date: 
                    print("doc, hl, date")
                    dt = datetime.strptime(date, '%Y-%m-%d')
                    records = db.session.execute(joinedStatement.where(Doctor.id == doc_id).where(Hospital.id == hl_id).where(MedicalRecord.created > dt).where(MedicalRecord.created < dt + timedelta(days=1)).order_by(MedicalRecord.created)).scalars()
                
    elif u_type == 'doctor':
        if pt_id:
            print("pt")
            records = db.session.execute(joinedStatement.where(Patient.id == pt_id).order_by(Hospital.name).order_by(MedicalRecord.created)).scalars()

            if date:
                print("pt, date")
                dt = datetime.strptime(date, '%Y-%m-%d')
                records = db.session.execute(joinedStatement.where(Hospital.id == hl_id).where(MedicalRecord.created > dt).where(MedicalRecord.created < dt + timedelta(days=1)).order_by(Patient.full_name)).scalars()
            
            if hl_id:
                print("pt, hl")
                records = db.session.execute(joinedStatement.where(Patient.id == pt_id).where(Hospital.id == hl_id).order_by(MedicalRecord.created)).scalars()

                if date:
                    print("pt, hl, date")
                    dt = datetime.strptime(date, '%Y-%m-%d')
                    records = db.session.execute(joinedStatement.where(Patient.id == pt_id).where(Hospital.id == hl_id).where(MedicalRecord.created > dt).where(MedicalRecord.created < dt + timedelta(days=1)).order_by(MedicalRecord.created)).scalars()

    else:
        records = None
    
    return render_template('main/mr_search.html', records = records)
    

@bp.route('/medical_record/id=<int:mr_id>')
@login_required
def medical_record(mr_id):
    # Ensure only the respective patient & doctor have access to the medical record
    record = db.session.execute(db.select(MedicalRecord).where(MedicalRecord.id == mr_id)).scalar()
    if record.patient.id != g.user.id or record.doctor.id != g.user.id:
        return render_template('error.html', e_code=403, e_text="Unauthorized")
    
    form = ExaminationForm()
    form2 = DiagnosisTreatmentForm()
    
    return render_template('main/medical_record.html', record = record, form = form, form2 = form2)