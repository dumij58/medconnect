from sqlalchemy import Column, Text, Integer, Date, Time, Numeric, DateTime, ForeignKey, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class MedicalHistory(db.Model):
    id = Column(Integer, primary_key=True)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    medical_condition = Column(Text)
    diagnosis_date = Column(Date)
    treatment = Column(Text)

class Medication(db.Model):
    id = Column(Integer, primary_key=True)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    medication_name = Column(Text)
    dosage = Column(Text)
    frequency = Column(Text)
    start_date = Column(Date)

class Surgery(db.Model):
    id = Column(Integer, primary_key=True)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    surgery_name = Column(Text)
    date = Column(Date)
    notes = Column(Text)

class Vaccination(db.Model):
    id = Column(Integer, primary_key=True)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    vaccine_name = Column(Text)
    administration_date = Column(Date)
    notes = Column(Text)

class FamilyHistory(db.Model):
    id = Column(Integer, primary_key=True)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    relationship = Column(Text)
    medical_condition = Column(Text)
    notes = Column(Text)


class Patient(db.Model):
    """ Data model for patient accounts """

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False, index=True)
    hash = Column(Text, nullable=False)
    full_name = Column(Text, nullable=False)
    gender = Column(Text, nullable=False)
    dob = Column(Date, nullable=False)
    contact = Column(Numeric, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    emergency_contact = Column(Numeric, nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)
    details_added = Column(Boolean, default=False, nullable=False)

    appointment = db.relationship('Appointment', back_populates='patient', lazy=True)
    medical_record = db.relationship('MedicalRecord', back_populates='patient', lazy=True)

    medical_history = db.relationship('MedicalHistory', lazy=True)
    current_medications = db.relationship('Medication', lazy=True)
    past_surgeries = db.relationship('Surgery', lazy=True)
    vaccinations = db.relationship('Vaccination', lazy=True)
    family_medical_history = db.relationship('FamilyHistory', lazy=True)

    def __repr__(self):
        return f'<Patient {self.username}>'


class Doctor(db.Model):
    """ Data model for doctor accounts """

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False, index=True)
    full_name = Column(Text, nullable=False)
    gender = Column(Text, nullable=False)
    dob = Column(Date, nullable=False)
    contact = Column(Numeric, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    specializations = Column(Text, nullable=True)
    reg_no = Column(Integer, unique=True, nullable=False)
    hash = Column(Text, nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)
    validated = Column(DateTime(timezone=False), nullable=False)

    appointment = db.relationship('Appointment', back_populates='doctor', lazy=True)
    medical_record = db.relationship('MedicalRecord', back_populates='doctor', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.username}>'
    

class DoctorPreVal(db.Model):
    """ Data model to store doctor data until validation """

    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    full_name = Column(Text, nullable=False)
    gender = Column(Text, nullable=False)
    dob = Column(Date, nullable=False)
    contact = Column(Numeric, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    specializations = Column(Text, nullable=True)
    reg_no = Column(Integer, unique=True, nullable=False)
    hash = Column(Text, nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)

    def __repr__(self):
        return f'<DoctorPreVal {self.id}>'
    

class Appointment(db.Model):
    """ Data model to store appointments """

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, unique=True, nullable=False)
    doc_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    hl_id = Column(Integer, ForeignKey('hospital.id'), nullable=False)
    s_id = Column(Integer, ForeignKey('doc_session.id'), nullable=False)
    status = Column(Text, nullable=False) # status - scheduled / ongoing / no_show / ended

    doctor = db.relationship('Doctor', back_populates='appointment', lazy=True)
    patient = db.relationship('Patient', back_populates='appointment', lazy=True)
    hospital = db.relationship('Hospital', back_populates='appointment', lazy=True)
    session = db.relationship('DocSession', back_populates='appointment', lazy=True)
    medical_record = db.relationship('MedicalRecord', back_populates='appointment', lazy=True)

    def __repr__(self):
        return f'<Appointment {self.id}>'
    

class DocSession(db.Model):
    """ Data model to store doctor sessions """

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    start_t = Column(Time, nullable=False)
    end_t = Column(Time, nullable=False)
    doc_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    hl_id = Column(Integer, ForeignKey('hospital.id'), nullable=False)
    total_apmts = Column(Integer, nullable=False)
    apmt_count = Column(Integer, nullable=False, default=0)

    doctor = db.relationship('Doctor', lazy=True)
    hospital = db.relationship('Hospital', lazy=True)
    appointment = db.relationship('Appointment', back_populates='session', lazy=True)

    def __repr__(self):
        return f'<DocSession {self.id}>'
    

class MedicalRecord(db.Model):
    """ Data model to store medical records """

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, nullable=False)
    doc_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    hl_id = Column(Integer, ForeignKey('hospital.id'), nullable=False)
    apmt_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    chief_complaint = Column(Text)
    diagnosis = Column(Text)
    follow_up_date = Column(Date)
    follow_up_notes = Column(Text)

    doctor = db.relationship('Doctor', back_populates='medical_record', lazy=True)
    patient = db.relationship('Patient', back_populates='medical_record', lazy=True)
    hospital = db.relationship('Hospital', back_populates='medical_record', lazy=True)
    appointment = db.relationship('Appointment', back_populates='medical_record', lazy=True)

    vital_signs = db.relationship('VitalSign', lazy=True)
    examination_notes = db.relationship('ExaminationNote', lazy=True)
    ordered_tests = db.relationship('OrderTest', lazy=True)
    treatment_medications = db.relationship('TreatmentMedications', lazy=True)
    treatment_other = db.relationship('TreatmentOther', lazy=True)
    referral = db.relationship('Referral', back_populates='medical_record', lazy=True)

    def __repr__(self):
        return f'<MedicalRecord {self.id}>'


class VitalSign(db.Model):
    """ Data model to store vital signs in a medical record """

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, ForeignKey('medical_record.id'), nullable=False)
    sign = Column(Text, nullable=False)
    value = Column(Text, nullable=False)

    def __repr__(self):
        return f'<VitalSign {self.id}>'
    

class ExaminationNote(db.Model):
    """ Data model to store examination notes in a medical record """

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, ForeignKey('medical_record.id'), nullable=False)
    title = Column(Text)
    notes = Column(Text)

    def __repr__(self):
        return f'<ExaminationNote {self.id}>'
    

class OrderTest(db.Model):
    """ Data model to store examination notes in a medical record """

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, ForeignKey('medical_record.id'), nullable=False)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    test_name = Column(Text, nullable=False)
    test_date = Column(Text, nullable=False)
    additional_notes = Column(Text)
    
    patient = db.relationship('Patient', lazy=True)
    medical_record = db.relationship('MedicalRecord', back_populates='ordered_tests', lazy=True)

    def __repr__(self):
        return f'<ExaminationNote {self.id}>'
    

class TreatmentMedications(db.Model):
    """ Data model to store treatments in a medical record """

    id = Column(Integer, primary_key=True)
    mr_id = Column(Integer, ForeignKey('medical_record.id'), nullable=False)
    medication_name = Column(Text)
    dosage = Column(Text)
    frequency = Column(Text)
    start_date = Column(Date)

    def __repr__(self):
        return f'<TreatmentMedications {self.id}>'
    

class TreatmentOther(db.Model):
    """ Data model to store treatments in a medical record """

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, ForeignKey('medical_record.id'), nullable=False)
    title = Column(Text)
    notes = Column(Text, nullable=False)

    def __repr__(self):
        return f'<TreatmentOther {self.id}>'
    

class Referral(db.Model):
    """ Data model to store referral form data """

    id = Column(Integer, primary_key=True, index=True)
    mr_id = Column(Integer, ForeignKey('medical_record.id'), nullable=False)
    date = Column(Date, nullable=False)
    doc_id = Column(Integer, ForeignKey('doctor.id'))
    external_doc_name = Column(Text)
    external_doc_specialization = Column(Text)
    reason = Column(Text, nullable=False)

    # Relationships
    doctor = db.relationship('Doctor', lazy=True)
    medical_record = db.relationship('MedicalRecord', back_populates='referral', lazy=True)

    def __repr__(self):
        return f'<Referral {self.id}>'


class Hospital(db.Model):
    """ Data model for hospitals """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    contact = Column(Numeric, nullable=False)

    appointment = db.relationship('Appointment', back_populates='hospital', lazy=True)
    medical_record = db.relationship('MedicalRecord', back_populates='hospital', lazy=True)

    def __repr__(self):
        return f'<Hospital {self.id}>'
    

class Admin(db.Model):
    """ Data model for admin accounts """

    id = Column(Integer, primary_key=True, index=True)
    identification_no = Column(Integer, nullable=False)
    username = Column(Text, unique=True, nullable=False)
    hash = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Admin {self.username}>'


class Contact(db.Model):
    """ Data model for contact form data """

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=False), nullable=False)
    name = Column(Text, nullable=False)
    user_type = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="unread")

    def __repr__(self):
        return f'<Contact {self.id}>'


class Log(db.Model):
    """ Data model for logs """

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=False), nullable=False)
    user = Column(Text)
    remarks = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Log {self.id}>'