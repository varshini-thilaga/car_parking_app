# Smart Parking Management System

A Django-based web application for managing parking slots.

## Features

- User registration and login
- View available parking slots
- Book parking slots
- View booking history
- Admin panel for managing slots and bookings

## Setup Instructions

1. Install Python and pip if not already installed.

2. Install Django:
   ```
   pip install django
   ```

3. Navigate to the project directory:
   ```
   cd "smart parking management system"
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and go to `http://127.0.0.1:8000/`

## Usage

- Register a new user or login with existing credentials.
- View available slots on the dashboard.
- Click "Book Now" on an available slot to book it.
- Enter your vehicle number and confirm.
- View your bookings and release slots when done.
- Admin can access `/admin/` to manage slots and view all bookings.

## Project Structure

```
smart_parking/
├── parking_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── smart_parking/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── booking.html
│   ├── register.html
│   └── registration/
│       └── login.html
├── static/
├── db.sqlite3
└── manage.py
```