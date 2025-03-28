from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import patch
from .models import Booking, Car
from django.contrib.auth.models import User
from datetime import datetime
from .models import Car, Booking, Payment
from datetime import datetime

class BookingTestCase(TestCase):

    def setUp(self):
        # Set up the necessary data for testing
        User = get_user_model()
        
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Create a car instance (make sure the owner is set properly)
        self.car = Car.objects.create(
            owner=self.user,  # Owner is the user created above
            model="Test Car",
            rental_price=100,
            year=1990,
            mileage=1000,
            pickup_location="Test Location",
            available_from=datetime(2025, 3, 28),  # Use datetime for date fields
            available_to=datetime(2025, 12, 31),  # Use datetime for date fields
        )

        # Create a booking instance with a non-confirmed booking
        self.booking = Booking.objects.create(
            renter=self.user,
            car=self.car,
            start_date=datetime(2025, 3, 29),
            end_date=datetime(2025, 4, 5),
            is_confirmed=False
        )
        
        # Create a booking instance with a confirmed booking
        self.confirmed_booking = Booking.objects.create(
            renter=self.user,
            car=self.car,
            start_date=datetime(2025, 4, 6),
            end_date=datetime(2025, 4, 10),
            is_confirmed=True
        )

    def test_booking_creation(self):
        # Test if bookings are correctly created
        self.assertEqual(self.booking.renter.username, 'testuser')
        self.assertEqual(self.booking.car.model, 'Test Car')
        self.assertEqual(self.booking.is_confirmed, False)

    def test_confirmed_booking(self):
        # Test if confirmed booking is correctly created
        self.assertEqual(self.confirmed_booking.renter.username, 'testuser')
        self.assertEqual(self.confirmed_booking.car.model, 'Test Car')
        self.assertEqual(self.confirmed_booking.is_confirmed, True)

    def test_booking_dates(self):
        # Test if the booking dates are correct
        self.assertEqual(self.booking.start_date, datetime(2025, 3, 29))
        self.assertEqual(self.booking.end_date, datetime(2025, 4, 5))

    def test_car_availability(self):
        # Test car availability within the given period
        car = self.car
        self.assertTrue(car.available_from <= self.booking.start_date <= car.available_to)
        self.assertTrue(car.available_from <= self.confirmed_booking.start_date <= car.available_to)
