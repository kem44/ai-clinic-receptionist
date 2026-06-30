from datetime import datetime, timedelta
from models import Appointment
from database import get_db



# DATE NORMALIZER

def normalize_date(date_text):
    if not date_text:
        return None

    text = str(date_text).lower().strip()

    if text == "today":
        return datetime.now().strftime("%Y-%m-%d")

    if text == "tomorrow":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    return str(date_text).strip()


# TIME NORMALIZER  

def normalize_time(time_text):
    if not time_text:
        return None

    text = str(time_text).upper().replace(" ", "")

    mapping = {
        "9AM": "9 AM",
        "10AM": "10 AM",
        "11AM": "11 AM",
        "12PM": "12 PM",
        "2PM": "2 PM",
        "3PM": "3 PM",
        "4PM": "4 PM",
        "5PM": "5 PM"
    }

    return mapping.get(text, str(time_text).strip())




# BOOK APPOINTMENT

def book_appointment(
    patient_name,
    patient_phone,
    patient_email,
    doctor_name,
    appointment_date,
    appointment_time
):
    print("=" * 50)
    print("patient_name:", repr(patient_name))
    print("patient_phone:", repr(patient_phone))
    print("patient_email:", repr(patient_email))
    print("doctor_name:", repr(doctor_name))
    print("appointment_date:", repr(appointment_date))
    print("appointment_time:", repr(appointment_time))
    print("=" * 50)

    if not all([patient_name, patient_phone, doctor_name, appointment_date, appointment_time]):
        return False, "Missing required booking details"

    appointment_date = normalize_date(appointment_date)
    appointment_time = normalize_time(appointment_time)

    if not appointment_date or not appointment_time:
        return False, "Invalid date or time"

    db = get_db()

    try:
        slots = available_slots(doctor_name, appointment_date)

        if appointment_time not in slots:
            return False, "Requested slot is unavailable"
        
        
        appointment = Appointment(
            patient_name=str(patient_name).strip(),
            patient_phone=str(patient_phone).strip(),
            patient_email=str(patient_email or "").strip(),
            doctor_name=str(doctor_name).strip(),
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            booking_status="CONFIRMED"
        )

        db.add(appointment)
        db.commit()

        return True, "Appointment booked successfully"

    except Exception as e:
        db.rollback()
        print("BOOK ERROR:", e)
        return False, "Booking failed"

    finally:
        db.close()


# CANCEL APPOINTMENT
def cancel_appointment(patient_name, patient_phone):
    db = get_db()
    try:
        appointment = ( 
            db.query(Appointment)
            .filter(
                Appointment.patient_name == str(patient_name).strip(),
                Appointment.patient_phone == str(patient_phone).strip(),
                Appointment.booking_status == "CONFIRMED"
            )
            .first()
        )

        if not appointment:
            return False, "No appointment found"
        
        appointment.booking_status = "CANCELLED"

        db.commit()
        
        return True, "Appointment cancelled sucessfully"
    

    except Exception as e:
        db.rollback()
        print("CANCEL ERROR:", str(e))
        return False, "Cancellation failed"
    
    finally:
        db.close()


# RESCHEDULE
def reschedule_appointment(patient_name, patient_phone, new_date, new_time):
    db = get_db()

    try:
        new_date = normalize_date(new_date)
        new_time = normalize_time(new_time)

        appointment = (
            db.query(Appointment)
            .filter(
                Appointment.patient_name == str(patient_name).strip(),
                Appointment.patient_phone == str(patient_phone).strip(),
                Appointment.booking_status == "CONFIRMED"
            )
            .first()
        )

        if not appointment:
            return False, "No appointment found"
        
        slots = available_slots(
            appointment.doctor_name,
            new_date
        )

        if new_time not in slots:
            return False, "Requessted slot is unavailable"
        
        appointment.appointment_date = new_date
        appointment.appointment_time = new_time

        db.commit()

        return True, "Appointment rescheduled successfully"


    except Exception as e:
        db.rollback()
        print("RESCHEDULE ERROR:", str(e))
        return False, "Reschedule failed"
    
    finally:
        db.close()


# FIND APPOINTMENT

def find_appointment(patient_name, patient_phone):
    db =get_db()
    
    try:
        appointment = (
            db.query(Appointment)
            .filter(
                Appointment.patient_name == str(patient_name).strip(),
                Appointment.patient_phone == str(patient_phone).strip(),
                Appointment.booking_status == "CONFIRMED"
            )
            .first()
        )

        if not appointment:
            return False, "No appointments found"
        return True, {
            "doctor_name": appointment.doctor_name,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
            "booking_status": appointment.booking_status
        }
    
    except Exception as e:
        print("FIND ERROR:", e)
        return False, "Lookup failed"
    
    finally:
        db.close()


# AVAILABLE SLOTS

def available_slots(doctor_name, appointment_date):
    try:
        appointment_date = normalize_date(appointment_date)

        all_slots = [
            "9 AM",
            "10 AM",
            "11 AM",
            "12 PM",
            "2 PM",
            "3 PM",
            "4 PM",
            "5 PM"
        ]

        db = get_db()
        
        booked = (
            db.query(Appointment)
            .filter(
                Appointment.doctor_name == doctor_name,
                Appointment.appointment_date == appointment_date,
                Appointment.booking_status == "CONFIRMED"
            )
            .all()
        )

        booked_slots = [a.appointment_time for a in booked]

        return [slot for slot in all_slots if slot not in booked_slots]

    except Exception as e:
        print("SLOT ERROR:", e)
        return[]
    
    finally:
        db.close()

