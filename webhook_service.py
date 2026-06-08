import requests


def trigger_booking_webhook(
    patient_name,
    doctor_name,
    appointment_date,
    appointment_time
):

    payload = {
        "patient_name": patient_name,
        "doctor_name": doctor_name,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time
    }

    response = requests.post(
        "http://127.0.0.1:5000/booking-webhook",
        json=payload
    )

    return response.status_code == 200