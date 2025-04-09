# DriveShare Project

## Introduction

DriveShare is a car rental platform that connects car owners with renters. Users can list, search, and book cars, while also managing bookings and payments. This project is built using Django and includes features like user authentication, booking notifications, and car management. It also allows renters and owners to message eachother with questions or concerns regarding a booking.

## Project Setup

## 1. Install Python 3.12.9
Make sure you have Python 3.12.9 installed. You can download it from https://www.python.org/downloads/release/python-3129/. 

Check mark the "Add python.exe to PATH" button during setup. You can check your Python version by running:
```bash
python --version
pip --version
```
Helpful note: If these commands don't work, make sure you add this Python version to PATH.
## 2. Install Visual Code
Install VS Code from: https://code.visualstudio.com/download

Install the Python extension from the Extensions tab (search for Python by Microsoft).

## 3. Install pipenv
If you don't have it already, run:
```bash
pip install pipenv
```
If that doesn't work, try:
```bash
python -m pip install pipenv
```
Or, make sure pip is installed and accessible from your terminal:
```bash
python -m ensurepip --upgrade
```

## 4. Clone the Project
Clone the repository to your local machine (can be inside a folder) and make sure you're in the car-rental-system directory:
```bash
git clone https://github.com/sabreenmun/car-rental-system.git
cd car-rental-system
```

## 5. Set up and activate the virtual environment using Python 3.12.9
If you have an older version of Python set as default, make sure to tell Pipenv to use Python 3.12.9:
```bash
pipenv --python 3.12.9
```
## 6. Install project dependencies
```bash
pipenv install
```
## 7. Activate the virtual environment in the directory where Pipfile and Pipfile.lock are located.
```bash
pipenv shell
```
## 8. Ensure these required dependencies are installed:
```bash
pipenv install Pillow djangorestframework
```

## 9. No need to set up database
The project uses SQLite with a preloaded db.sqlite3 file.

Note: If you'd like to use your own database in the future (like PostgreSQL or MySQL), you can update the DATABASES setting in car_rental/settings.py with your new configuration and credentials.

## 10. Run migrations if needed (optional)
```bash
python manage.py migrate
```

## 11. Start the Django development server
```bash
python manage.py runserver
```

## 12. Visit the website in your browser:
**URL**: http://127.0.0.1:8000/


## 13. Login Credentials
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

Feel free to explore DriveShare — add new users, upload cars, exchange messages, and get a feel for how our platform works. 

## Thank You
Thank you for checking DriveShare out! - Sabreen, Reem, Doha, Mariam
