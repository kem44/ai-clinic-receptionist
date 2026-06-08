import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import uuid


# -------------------------
# SHEET CONNECTION
# -------------------------
def connect_sheet():
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    return client.open("CarePlus_Appointments").sheet1


# -------------------------
# DATE NORMALIZER
# -------------------------
def normalize_date(date_text):
    if not date_text:
        return None

    text = str(date_text).lower().strip()

    if text == "today":
        return datetime.now().strftime("%Y-%m-%d")

    if text == "tomorrow":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    return str(date_text).strip()


# -------------------------
# TIME NORMALIZER (IMPORTANT)
# -------------------------
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


# -------------------------
# SLOT CHECK
# -------------------------
def slot_available(sheet, doctor, date, time):
    records = sheet.get_all_records()

    doctor = str(doctor).strip()
    date = str(date).strip()
    time = str(time).strip()

    for record in records:
        if (
            str(record.get("doctor_name", "")).strip() == doctor
            and str(record.get("appointment_date", "")).strip() == date
            and str(record.get("appointment_time", "")).strip() == time
            and str(record.get("booking_status", "")).strip() == "CONFIRMED"
        ):
            return False

    return True


# -------------------------
# BOOK APPOINTMENT
# -------------------------
def book_appointment(
    patient_name,
    patient_phone,
    patient_email,
    doctor_name,
    appointment_date,
    appointment_time
):
    
    print("patient_name =", patient_name)
    print("patient_phone =", patient_phone)
    print("patient_email =", patient_email)
    print("doctor_name =", doctor_name)
    print("appointment_date =", appointment_date)
    print("appointment_time =", appointment_time)
    try:
        # ---------------- VALIDATION ----------------
        if not all([patient_name, patient_phone, doctor_name, appointment_date, appointment_time]):
            return False, "Missing required booking details"

        sheet = connect_sheet()

        # ---------------- NORMALIZATION ----------------
        appointment_date = normalize_date(appointment_date)
        appointment_time = normalize_time(appointment_time)

        if not appointment_date or not appointment_time:
            return False, "Invalid date or time"

        # ---------------- SLOT CHECK ----------------
        if not slot_available(sheet, doctor_name, appointment_date, appointment_time):
            return False, "Selected slot is unavailable"

        # ---------------- INSERT ----------------
        sheet.append_row([
            str(uuid.uuid4())[:8],
            str(patient_name).strip(),
            str(patient_phone).strip(),
            str(patient_email or "").strip(),
            str(doctor_name).strip(),
            appointment_date,
            appointment_time,
            "CONFIRMED",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

        return True, "Appointment booked successfully"

    except Exception as e:
        print("BOOK ERROR:", str(e))
        return False, "Booking failed"


# -------------------------
# CANCEL APPOINTMENT
# -------------------------
def cancel_appointment(patient_name, patient_phone):
    try:
        sheet = connect_sheet()
        records = sheet.get_all_records()

        for index, record in enumerate(records, start=2):

            if (
                str(record.get("patient_name", "")).strip() == str(patient_name).strip()
                and str(record.get("patient_phone", "")).strip() == str(patient_phone).strip()
                and str(record.get("booking_status", "")).strip() == "CONFIRMED"
            ):
                sheet.update_cell(index, 8, "CANCELLED")
                return True, "Appointment cancelled successfully"

        return False, "No appointment found"

    except Exception as e:
        print("CANCEL ERROR:", str(e))
        return False, "Cancellation failed"


# -------------------------
# RESCHEDULE
# -------------------------
def reschedule_appointment(patient_name, patient_phone, new_date, new_time):
    try:
        sheet = connect_sheet()

        new_date = normalize_date(new_date)
        new_time = normalize_time(new_time)

        records = sheet.get_all_records()

        for index, record in enumerate(records, start=2):

            if (
                str(record.get("patient_name", "")).strip() == str(patient_name).strip()
                and str(record.get("patient_phone", "")).strip() == str(patient_phone).strip()
                and str(record.get("booking_status", "")).strip() == "CONFIRMED"
            ):
                doctor = record.get("doctor_name")

                if not slot_available(sheet, doctor, new_date, new_time):
                    return False, "Requested slot is unavailable"

                sheet.update_cell(index, 6, new_date)
                sheet.update_cell(index, 7, new_time)

                return True, "Appointment rescheduled successfully"

        return False, "No appointment found"

    except Exception as e:
        print("RESCHEDULE ERROR:", str(e))
        return False, "Reschedule failed"


# -------------------------
# FIND APPOINTMENT
# -------------------------
def find_appointment(patient_name, patient_phone):
    try:
        sheet = connect_sheet()
        records = sheet.get_all_records()

        for record in records:
            if (
                str(record.get("patient_name", "")).strip() == str(patient_name).strip()
                and str(record.get("patient_phone", "")).strip() == str(patient_phone).strip()
                and str(record.get("booking_status", "")).strip() == "CONFIRMED"
            ):
                return True, {
                    "doctor_name": record.get("doctor_name"),
                    "appointment_date": record.get("appointment_date"),
                    "appointment_time": record.get("appointment_time"),
                    "booking_status": record.get("booking_status")
                }

        return False, "No appointment found"

    except Exception as e:
        print("FIND ERROR:", str(e))
        return False, "Lookup failed"


# -------------------------
# AVAILABLE SLOTS
# -------------------------
def available_slots(doctor_name, appointment_date):
    try:
        all_slots = ["9 AM", "10 AM", "11 AM", "12 PM", "2 PM", "3 PM", "4 PM", "5 PM"]

        sheet = connect_sheet()
        records = sheet.get_all_records()

        doctor_name = str(doctor_name).strip()
        appointment_date = str(appointment_date).strip()

        booked_slots = []

        for record in records:
            if (
                str(record.get("doctor_name", "")).strip() == doctor_name
                and str(record.get("appointment_date", "")).strip() == appointment_date
                and str(record.get("booking_status", "")).strip() == "CONFIRMED"
            ):
                booked_slots.append(record.get("appointment_time"))

        return [slot for slot in all_slots if slot not in booked_slots]

    except Exception as e:
        print("SLOTS ERROR:", str(e))
        return []