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

    # Relationships
    medical_history = db.relationship('MedicalHistory', backref='patient', lazy=True)
    current_medications = db.relationship('Medication', backref='patient', lazy=True)
    past_surgeries = db.relationship('Surgery', backref='patient', lazy=True)
    vaccinations = db.relationship('Vaccination', backref='patient', lazy=True)
    family_medical_history = db.relationship('FamilyHistory', backref='patient', lazy=True)

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
    specialities = Column(Text, nullable=True)
    reg_no = Column(Integer, unique=True, nullable=False)
    hash = Column(Text, nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)
    validated = Column(DateTime(timezone=False), nullable=False)

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
    specialities = Column(Text, nullable=True)
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

    def __repr__(self):
        return f'<Appointment {self.id}>'
    

class DocSession(db.Model):
    """ Data model to store doctor available time """

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    start_t = Column(Time, nullable=False)
    end_t = Column(Time, nullable=False)
    doc_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    hl_id = Column(Integer, ForeignKey('hospital.id'), nullable=False)
    total_apmts = Column(Integer, nullable=False)
    apmt_count = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<DocSession {self.id}>'
    

class MedicalRecords(db.Model):
    """ Data model to store appointments """

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, unique=True, nullable=False)
    doc_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    hl_id = Column(Integer, ForeignKey('hospital.id'), nullable=False)
    file = Column(Text, unique=True, nullable=False)
    passkey = Column(Text, unique=True, nullable=False)

    def __repr__(self):
        return f'<Appointment {self.id}>'


class Hospital(db.Model):
    """ Data model for hospitals """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    contact = Column(Numeric, nullable=False)

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
    

class Log(db.Model):
    """ Data model for logs """

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=False), nullable=False)
    user = Column(Text)
    remarks = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Log {self.id}>'