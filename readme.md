# AI Voice Receptionist with Retell AI + Flask + PostgreSQL

## Overview

This project is an AI-powered voice receptionist that automates clinic appointment management. It integrates Retell AI with a Flask backend and PostgreSQL database to handle appointment booking, lookup, cancellation, rescheduling, and slot availability.

The project was initially prototyped using Google Sheets and later migrated to PostgreSQL to improve scalability, reliability, and maintainability.

---

## Features

- Book appointments
- Check available appointment slots
- Find existing appointments
- Cancel appointments
- Reschedule appointments
- REST API endpoints
- PostgreSQL database
- SQLAlchemy ORM
- Environment variable configuration

---

## Tech Stack

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Retell AI
- ngrok
- python-dotenv

---

## Project Structure

```
AI-Receptionist/
│
├── app.py
├── booking_engine.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env (not committed)
```

---

## Architecture

```
Retell AI
     │
     ▼
 Flask API
     │
     ▼
Business Logic
(booking_engine.py)
     │
     ▼
SQLAlchemy ORM
     │
     ▼
PostgreSQL
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /book-appointment | Book appointment |
| POST | /find-appointment | Find appointment |
| POST | /available-slots | Get available slots |
| POST | /cancel-appointment | Cancel appointment |
| POST | /reschedule-appointment | Reschedule appointment |

---

## Why PostgreSQL?

Google Sheets was suitable for rapid prototyping but has limitations for production systems.

PostgreSQL was chosen because it provides:

- Reliable transactional storage
- Better performance
- Concurrent access support
- Data integrity
- Scalability
- Industry-standard relational database features

---

## Future Improvements

- Multi-clinic support
- Multi-business AI receptionist platform
- Calendar integration
- Email/SMS notifications
- Authentication
- Admin dashboard
- Docker deployment
- Cloud deployment

---

## Learning Outcomes

This project demonstrates:

- REST API development with Flask
- Database modeling using SQLAlchemy
- PostgreSQL integration
- Environment variable management
- Backend architecture and separation of concerns
- AI voice agent integration