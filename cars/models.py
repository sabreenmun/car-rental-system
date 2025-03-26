from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

class Car(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    model = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    year = models.IntegerField()
    mileage = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    pickup_location = models.CharField(max_length=255)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_dates = models.JSONField(default=list)  # Store available dates as a list of strings
    created_at = models.DateTimeField(auto_now_add=True)

    def is_available(self, start_date, end_date):
        """Check if all requested dates are available."""
        requested_dates = self.get_date_range(start_date, end_date)
        return all(date in self.available_dates for date in requested_dates)

    def get_date_range(self, start_date, end_date):
        """Generate list of date strings from start_date to end_date."""
        return [str(start_date + timedelta(days=i)) for i in range((end_date - start_date).days + 1)]

    def __str__(self):
        return f"{self.model} ({self.year}) - {self.owner.username}"

    
class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE ,  related_name="bookings")
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # নতুন যোগ করা হয়েছে

    def __str__(self):
        return f"Booking: {self.car.model} from {self.start_date} to {self.end_date}"

    def is_conflicting(self):
        existing_bookings = Booking.objects.filter(car=self.car, is_confirmed=True)
        for booking in existing_bookings:
            if (self.start_date <= booking.end_date) and (self.end_date >= booking.start_date):
                return True
        return False





class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")],
        default="pending",
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.car.model} - {self.status}"




    
class CarBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100, choices=[('booked', 'Booked'), ('completed', 'Completed')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Rental(models.Model):
    car_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_cars', on_delete=models.CASCADE)
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rented_cars', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)  
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rental of {self.car} by {self.renter.username}"