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
from .forms import *

User = get_user_model()

class CarSearchTestCase(TestCase):
    
    def setUp(self):
        # Create a user to associate with the car
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create some Car instances to search through
        self.car1 = Car.objects.create(
            owner=self.user,
            model="Toyota Camry",
            image="images/toyota_camry.jpg",  # You may need to mock or adjust the image path for tests
            year=2020,
            mileage=15000,
            pickup_location="New York",
            rental_price=49.99,
            available_from=date(2023, 5, 1),
            available_to=date(2023, 12, 31),
        )

        self.car2 = Car.objects.create(
            owner=self.user,
            model="Honda Accord",
            image="images/honda_accord.jpg",  # Mock or adjust for testing
            year=2021,
            mileage=10000,
            pickup_location="Los Angeles",
            rental_price=59.99,
            available_from=date(2023, 6, 1),
            available_to=date(2023, 11, 30),
        )
        
        self.car3 = Car.objects.create(
            owner=self.user,
            model="Ford Mustang",
            image="images/ford_mustang.jpg",  # Mock or adjust for testing
            year=2019,
            mileage=20000,
            pickup_location="Chicago",
            rental_price=69.99,
            available_from=date(2023, 4, 1),
            available_to=date(2023, 9, 30),
        )

    def test_search_with_valid_input(self):
        # Log in the user
        self.client.login(username="testuser", password="password")

        # Send a GET request to search for cars with model 'Toyota' and year '2020'
        response = self.client.get('/cars/', {'model': 'Toyota', 'year': 2020})

        # Check that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check that the car with model 'Toyota Camry' appears in the response content
        self.assertContains(response, 'Toyota Camry')

        # Check that cars that do not match the criteria do not appear in the response
        self.assertNotContains(response, 'Honda Accord')
        self.assertNotContains(response, 'Ford Mustang')

    def test_search_with_no_results(self):
        # Log in the user
        self.client.login(username="testuser", password="password")

        # Search with a model that doesn't exist
        response = self.client.get('/cars/', {'model': 'Nonexistent Model', 'year': 2025})

        # Check that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check that no cars appear in the response
        self.assertNotContains(response, 'Toyota Camry')
        self.assertNotContains(response, 'Honda Accord')
        self.assertNotContains(response, 'Ford Mustang')