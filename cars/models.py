from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

#model for the Car
class Car(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    model = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    year = models.IntegerField()
    mileage = models.PositiveIntegerField()
    pickup_location = models.CharField(max_length=255)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()  # Car availability start date
    available_to = models.DateField()    # Car availability end date
    created_at = models.DateTimeField(auto_now_add=True)


    def is_available(self, start_date, end_date):
        """check if dates fall within the car's availability range and aren't booked."""
        if not (self.available_from <= start_date and self.available_to >= end_date):
            return False  #outside availability range
        
        #maek sure no overlapping bookings
        overlapping_bookings = self.bookings.filter(
            is_confirmed=True,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists()
        
        return not overlapping_bookings

    def __str__(self):
        return f"{self.model} ({self.year}) - {self.owner.username}"

#model for the Booking
class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return f"Booking: {self.car.model} from {self.start_date} to {self.end_date}"

    def is_conflicting(self):
        """Check if the booking conflicts with existing confirmed bookings."""
        return Booking.objects.filter(
            car=self.car,
            is_confirmed=True,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exists()

#model for the Payment aka the Invoice
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


#unused. delete later!
class CarBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100, choices=[('booked', 'Booked'), ('completed', 'Completed')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

#unused! delete later!
class Rental(models.Model):
    car_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_cars', on_delete=models.CASCADE)
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rented_cars', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)  
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rental of {self.car} by {self.renter.username}"