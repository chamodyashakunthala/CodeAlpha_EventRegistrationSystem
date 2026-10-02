# CodeAlpha Event Registration System

Backend for managing events and user registrations, built with Django and Django REST Framework as part of the CodeAlpha Backend Development Internship (Task 2).

## Features

- Event list and event detail endpoints
- Live `seats_available` count (capacity minus confirmed registrations)
- Registration for logged-in users, with duplicate and full-event checks
- View your own registrations and cancel them
- Cancelled users can register again (the old record is reactivated)
- Admin panel for organizers to manage events and registrations

## Tech Stack

Python, Django 6, Django REST Framework, SQLite

## Setup

```bash
git clone <this-repo-url>
cd CodeAlpha_EventRegistrationSystem
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Log in at `http://127.0.0.1:8000/admin/` to add events and users.

## API Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/api/events/` | No | List all events |
| GET | `/api/events/<id>/` | No | Event details with seats available |
| POST | `/api/events/<id>/register/` | Yes | Register the logged-in user |
| GET | `/api/registrations/` | Yes | List my registrations |
| POST | `/api/registrations/<id>/cancel/` | Yes | Cancel one of my registrations |

## Data Models

- **Event:** title, description, location, date, capacity
- **Registration:** user, event, status (confirmed/cancelled); one record per user and event