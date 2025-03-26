from django.conf import settings
from django.db import models

class CarOwner(models.Model):
    SECURITY_QUESTIONS = [
        ("first_pet", "What was the name of your first pet?"),
        ("mother_maiden", "What is your mother’s maiden name?"),
        ("first_car", "What was the model of your first car?"),
        ("favorite_movie", "What is your favorite movie?"),
        ("childhood_friend", "What is the name of your childhood best friend?"),
        ("high_school", "What high school did you attend?"),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    security_question_1 = models.CharField(max_length=50, choices=SECURITY_QUESTIONS)
    security_answer_1 = models.CharField(max_length=255)
    security_question_2 = models.CharField(max_length=50, choices=SECURITY_QUESTIONS)
    security_answer_2 = models.CharField(max_length=255)
    security_question_3 = models.CharField(max_length=50, choices=SECURITY_QUESTIONS)
    security_answer_3 = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username



