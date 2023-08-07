from sqlalchemy import Column, Text, Integer, Date, Time, Numeric, DateTime, Boolean, ForeignKey

from . import db

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
    medical_history = Column(Text, nullable=True)
    created = Column(DateTime(timezone=False), nullable=False)

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
    dr_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)  ## Change dr_id to doc_id for consistancy
    pt_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
    hl_id = Column(Integer, ForeignKey('hospital.id'), nullable=False)

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

    def __repr__(self):
        return f'<DocSession {self.id}>'


class Hospital(db.Model):
    """ Data model for hospitals """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
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