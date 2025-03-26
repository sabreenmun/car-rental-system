from django.urls import path
from .views import *



urlpatterns = [
    path('', home, name='home'),
    path('car_owner_register/', car_owner_register, name='car_owner_register'),
    path('car_owner_login/', car_owner_login, name='car_owner_login'),
    path('reset-password/', request_password_reset, name='request_password_reset'),
    path('verify-security-questions/', verify_security_questions, name='verify_security_questions'),
    path('set-new-password/', set_new_password, name='set_new_password'),
    path('login_choice/', login_choice, name='login_choice'),
    path('register_choice/', register_choice, name='register_choice'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('help/', help, name='help'),


]