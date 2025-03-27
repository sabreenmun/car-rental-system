from django.urls import path
from .views import *   
from . import views

urlpatterns = [
    path('car-renter-register/', views.car_renter_register, name='car_renter_register'),
    path('car-renter-login/', views.car_renter_login, name='car_renter_login'),
    path('request-password-reset/', views.request_password_reset, name='car_renter_request_password_reset'),
    path('verify-security-questions/', views.verify_security_questions, name='car_renter_verify_security_questions'),
    path('set-new-password/', views.set_new_password, name='car_renter_set_new_password'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile')
]
