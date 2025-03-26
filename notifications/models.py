from django.db import models
from cars.models import Car
from django.conf import settings
from cars.models import Booking

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"



class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  # No default datetime
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_reviews")
    reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_reviews")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "booking")  # Ensures a user can review a booking only once

    def __str__(self):
        return f"Review by {self.reviewer} for {self.reviewed_user} on {self.booking.car.model}"

