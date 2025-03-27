from django.conf import settings
from django.db import models

class CarOwner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    security_question_1 = models.CharField(max_length=255)
    security_answer_1 = models.CharField(max_length=255)
    security_question_2 = models.CharField(max_length=255)
    security_answer_2 = models.CharField(max_length=255)
    security_question_3 = models.CharField(max_length=255)
    security_answer_3 = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username



