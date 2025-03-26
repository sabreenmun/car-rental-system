from django.contrib import admin

from .models import *

admin.site.register(Car)

admin.site.register(Booking)
admin.site.register(CarBooking)
admin.site.register(Rental)

