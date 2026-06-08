# AI Clinic Receptionist

AI-powered clinic receptionist built using RetellAI Conversational Flow and Python automation.

## Features

* Appointment booking
* Appointment cancellation
* Appointment rescheduling
* Appointment lookup
* FAQ handling
* Human escalation
* Google Sheets integration
* Webhook support

## Tech Stack

* RetellAI
* Python
* Flask
* Google Sheets API
* Ngrok

## Setup

1. Clone repository
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Add Google Service Account credentials

```text
credentials.json
```

4. Run application

```bash
python app.py
```

5. Expose locally using ngrok

```bash
ngrok http 5000
```

## Project Structure

* app.py → Flask API
* booking_engine.py → Appointment logic
* webhook_service.py → Booking webhook
* agent.json → RetellAI conversational flow export
