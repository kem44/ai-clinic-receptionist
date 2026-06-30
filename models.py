from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String, nullable=False)
    patient_phone = Column(String, nullable=False)
    patient_email = Column(String)

    doctor_name = Column(String, nullable=False)

    appointment_date = Column(String, nullable=False)
    appointment_time = Column(String, nullable=False)

    booking_status = Column(String, default="CONFIRMED")