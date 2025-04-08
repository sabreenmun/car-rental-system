from django.contrib import admin
from .models import *
#for admin models
admin.site.register(Message)
admin.site.register(Conversation)