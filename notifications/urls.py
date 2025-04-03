
from django.urls import path
from .views import *

urlpatterns = [
    path('', notifications, name='notifications'),
    path('notification/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path("review/<int:booking_id>/", submit_review, name="submit_review"),
    path("extra/", extra, name="extra"),
    
]