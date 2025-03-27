from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import patch
from .models import Car, Booking, Payment

class PaymentViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.car = Car.objects.create(
            owner=self.user,
            model="Corolla",
            image="images/test.jpg",
            year=2020,
            mileage=15000,
            availability=True,
            pickup_location="123 Main Street",
            rental_price=50.00,
            available_dates=["2024-04-01", "2024-04-02"],
        )

        self.booking = Booking.objects.create(
            car=self.car,
            renter=self.user,
            start_date="2024-04-01",
            end_date="2024-04-05",
            total_price=200.00,
            is_confirmed=False,
        )

    @patch("cars.views.PaymentGatewayProxy.process_payment")  # Mock payment processing
    def test_process_payment_success(self, mock_process_payment):
        mock_process_payment.return_value = {"status": "completed", "transaction_id": "TXN12345"}

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("process_payment", args=[self.booking.id]))

        self.booking.refresh_from_db()
        self.assertTrue(self.booking.is_confirmed)  # Ensure booking is confirmed
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Check payment record was created
        payment = Payment.objects.get(booking=self.booking)
        self.assertEqual(payment.status, "completed")

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Payment successful!", str(messages[0]))

    @patch("cars.views.PaymentGatewayProxy.process_payment")  # Mock payment failure
    def test_process_payment_failure(self, mock_process_payment):
        mock_process_payment.return_value = {"status": "failed", "transaction_id": "TXN67890"}

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("process_payment", args=[self.booking.id]))

        self.booking.refresh_from_db()
        self.assertFalse(self.booking.is_confirmed)  # Booking should NOT be confirmed

        # Check payment record was created
        payment = Payment.objects.get(booking=self.booking)
        self.assertEqual(payment.status, "failed")

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Payment failed!", str(messages[0]))
