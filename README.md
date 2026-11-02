# MyNotes - Productivity App API

## Project Description

MyNotes is a Flask REST API that allows users
to manage personal notes securely.

Users can register, log in, create notes,
view notes, update notes and delete notes.

The application uses session-based authentication
to protect private user information.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Flask-Bcrypt
- Flask-Migrate
- Pytest

## Features

1. User registration
2. Secure password hashing
3. Session-based authentication
4. Login and logout
5. Session checking
6. Notes CRUD operations
7. User-specific access control
8. Pagination
9. Database seeding

## Installation

Clone the repository:

    git clone YOUR_GITHUB_REPOSITORY_URL

Navigate into the project:

    cd productivity-app

Install dependencies:

    pipenv install --dev

## Database Setup

Seed the database:

    pipenv run python seed.py

## Run the Application

    pipenv run flask --app run.py run --debug

The application runs at:

    http://127.0.0.1:5000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup | Register user |
| POST | /login | Login |
| DELETE | /logout | Logout |
| GET | /check_session | Check session |
| GET | /notes | Get all notes |
| POST | /notes | Create note |
| GET | /notes/<id> | Get one note |
| PATCH | /notes/<id> | Update note |
| DELETE | /notes/<id> | Delete note |

## Pagination

Example:

    GET /notes?page=1&per_page=5

## Authentication

Passwords are hashed using Flask-Bcrypt.

Sessions are used to authenticate users.

Users can only access their own notes.

## Testing

Run tests:

    pipenv run pytest

## Demo Account

Username: demo_user

Password: Password123!

## Author

Rihanna Tanya