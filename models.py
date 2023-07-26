from sqlalchemy import Column, String, Text, Integer, Date, Numeric, DateTime

from . import db

class Patient(db.Model):
    """ Data model for patient accounts """

    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False, index=True)
    full_name = Column(Text, nullable=False)
    dob = Column(Date, nullable=False)
    contact = Column(Numeric, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    hash = Column(Text, nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)

    def __repr__(self):
        return f'<Patient {self.username}>'