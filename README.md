# DriveShare Project

## Introduction

DriveShare is a car rental platform that connects car owners with renters. Users can list, search, and book cars, while also managing bookings and payments. This project is built using Django and includes features like user authentication, booking notifications, and car management. It also allows renters and owners to message eachother with questions or concerns regarding a booking.

## Project Setup

## 1. Clone the Project
Clone the repository to your local machine:
```bash
git clone https://github.com/sabreenmun/car-rental-system.git
```

## 2. Install Python 3.12.9
Make sure you have Python 3.12.9 installed. You can check your Python version by running:
```bash
python --version
```
If it's not 3.12.9, download and install it from: https://www.python.org/downloads/release/python-3129/

## 3. Install pipenv
If you don't have it already, run:
```bash
pip install pipenv
```
## 4. Set up and activate the virtual environment using Python 3.12.9
If you have an older version of Python set as default, explicitly tell Pipenv to use Python 3.12.9:
```bash
pipenv --python 3.12.9
```
## 5. Install project dependencies
```bash
pipenv install
```
## 6. Activate the virtual environment in the directory where Pipfile and Pipfile.lock are located.
```bash
pipenv shell
```
## 7. Ensure these required dependencies are installed:
```bash
pipenv install Pillow djangorestframework
```

## 8. No need to set up MySQL
The project uses SQLite with a preloaded db.sqlite3 file

## 9. Run migrations if needed (optional)
```bash
python manage.py migrate
```

## 10. Start the Django development server
```bash
python manage.py runserver
```

## 11. Visit the app in your browser:
**URL**: http://127.0.0.1:8000/


## 12. Login Credentials
### Admin Panel (to view models or add/remove data)
- **URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username**: `test`
- **Password**: `test`

### Owner Account
- **Username**: `jonsnow`
- **Password**: `jonsnow`
- **Details**: Owner has 3 car listings posted.

### Renter Account
- **Username**: `mary`
- **Password**: `mary`
- **Details**: Renter has the following bookings:
  - Ongoing booking
  - Reserved a booking without paying (confirmed)
  - Completed booking (with review)
  - Future booking
