from django.urls import path
from .views import *

urlpatterns = [
    path('', car_list, name="car_list"),
    path("add/", car_create, name="car_create"),
    path('update/<int:pk>/', CarUpdateView.as_view(), name='car_update'),
    path("delete/<int:car_id>/", car_delete, name="car_delete"),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path("book/<int:car_id>/", book_car, name="book_car"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    
    path('search/', car_search, name='car_search'),
    path("payment-status/<int:booking_id>/", payment_status, name="payment_status"),
    path("payment/<int:booking_id>/", process_payment, name="process_payment"),
]
