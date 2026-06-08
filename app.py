from flask import Flask, request, jsonify

from booking_engine import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment,
    find_appointment,
    available_slots
)

app = Flask(__name__)


@app.route("/")
def home():
    return "Clinic Receptionist API Running"


# -------------------------
# BOOK APPOINTMENT
# -------------------------
@app.route("/book-appointment", methods=["POST"])
def create_appointment():

    try:
        data = request.json or {}

        print("\nBOOK APPOINTMENT REQUEST")
        print(data)

        args = data.get("args", {}).get("args", {})

        success, message = book_appointment(
            patient_name=args.get("patient_name"),
            patient_phone=args.get("patient_phone"),
            patient_email=args.get("patient_email"),
            doctor_name=args.get("doctor_name"),
            appointment_date=args.get("appointment_date"),
            appointment_time=args.get("appointment_time")
        )

        return jsonify({
            "status": "success" if success else "failed",
            "message": message
        })

    except Exception as e:

        print("BOOK ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "message": "Server error"
        }), 500


# -------------------------
# CANCEL APPOINTMENT
# -------------------------
@app.route("/cancel-appointment", methods=["POST"])
def cancel_booking():

    try:
        data = request.json or {}
        args = data.get("args", {}).get("args", {})

        success, message = cancel_appointment(
            patient_name=args.get("patient_name"),
            patient_phone=args.get("patient_phone")
        )

        return jsonify({
            "status": "success" if success else "failed",
            "message": message
        })

    except Exception as e:

        print("CANCEL ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "message": "Server error"
        }), 500


# -------------------------
# RESCHEDULE
# -------------------------
@app.route("/reschedule-appointment", methods=["POST"])
def reschedule_booking():

    try:
        data = request.json or {}
        args = data.get("args", {}).get("args", {})

        success, message = reschedule_appointment(
            patient_name=args.get("patient_name"),
            patient_phone=args.get("patient_phone"),
            new_date=args.get("new_date"),
            new_time=args.get("new_time")
        )

        return jsonify({
            "status": "success" if success else "failed",
            "message": message
        })

    except Exception as e:

        print("RESCHEDULE ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "message": "Server error"
        }), 500


# -------------------------
# FIND APPOINTMENT
# -------------------------
@app.route("/find-appointment", methods=["POST"])
def lookup_appointment():

    try:
        data = request.json or {}
        args = data.get("args", {}).get("args", {})
        success, result = find_appointment(
            patient_name=args.get("patient_name"),
            patient_phone=args.get("patient_phone")
        )

        return jsonify({
            "status": "success" if success else "failed",
            "result": result
        })

    except Exception as e:

        print("FIND ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "result": "Server error"
        }), 500


# -------------------------
# AVAILABLE SLOTS
# -------------------------
@app.route("/available-slots", methods=["POST"])
def get_available_slots():

    try:
        data = request.json or {}
        args = data.get("args", {}).get("args", {})
        slots = available_slots(
            doctor_name=args.get("doctor_name"),
            appointment_date=args.get("appointment_date")
        )

        return jsonify({
            "status": "success",
            "available_slots": slots
        })

    except Exception as e:

        print("SLOTS ERROR:", str(e))

        return jsonify({
            "status": "failed",
            "available_slots": []
        }), 500


# -------------------------
# WEBHOOK
# -------------------------
@app.route("/booking-webhook", methods=["POST"])
def booking_webhook():

    data = request.json

    print("\nWEBHOOK RECEIVED")
    print(data)

    return jsonify({
        "status": "received"
    })


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)