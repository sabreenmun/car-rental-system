from django.db import models
from cars.models import Car
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"


# models.py
from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Review(models.Model):
    car = models.ForeignKey("cars.Car", on_delete=models.CASCADE, related_name="reviews")  # Car being reviewed
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_reviews")
    reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_reviews")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "car")  # A user can review a car only once

    def __str__(self):
        return f"Review by {self.reviewer} for {self.reviewed_user} on {self.car}"


