
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from cars.models import Car

class Conversation(models.Model):
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='renter_conversations', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_conversations', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='conversations', on_delete=models.CASCADE)
    last_message = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {self.renter} and {self.owner} for {self.car}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.text}"
