from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('renter', 'Car Renter'),
        ('owner', 'Car Owner'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='renter')  

class CarRenter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    security_question_1 = models.CharField(max_length=255)
    security_answer_1 = models.CharField(max_length=255)
    security_question_2 = models.CharField(max_length=255)
    security_answer_2 = models.CharField(max_length=255)
    security_question_3 = models.CharField(max_length=255)
    security_answer_3 = models.CharField(max_length=255)

    class Meta:
        db_table = 'users_carrenter'

    def __str__(self):
        return self.user.username


