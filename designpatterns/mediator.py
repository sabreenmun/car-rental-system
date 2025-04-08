#This is where the mediator pattern functionality goes.
from django.db.models import Q
from django.contrib import messages
from cars.models import Booking

#mediator
class BookingMediatorInterface:
    def process_booking(self):
        raise NotImplementedError

#concrete mediator
class BookingMediator(BookingMediatorInterface):
    def __init__(self, request, car, form):
        self.request = request
        self.car = car
        self.form = form
        self.booking = None
    #main method to process the booking
    def process_booking(self):
        self.booking = self.form.save(commit=False)
        self.booking.car = self.car
        self.booking.renter = self.request.user

        #check if car has those dates available
        if not self._is_within_availability():
            messages.error(self.request, "Selected dates are outside the car's availability range.")
            return False

        #check if overlaps w another booking
        if self._has_conflicts():
            messages.error(self.request, "This car is already booked for the selected dates.")
            return False

        #check if start date before end date
        if not self._is_duration_valid():
            messages.error(self.request, "End date must be after start date.")
            return False
        
        # finalize the booking if all checks pass
        self._finalize_booking()
        return True

    def _is_within_availability(self):
        return (self.car.available_from <= self.booking.start_date and 
                self.car.available_to >= self.booking.end_date)

    def _has_conflicts(self):
        return Booking.objects.filter(
            car=self.car,
            is_confirmed=True,
        ).filter(
            Q(start_date__lt=self.booking.end_date) & Q(end_date__gt=self.booking.start_date)
        ).exists()

    def _is_duration_valid(self):
        total_days = (self.booking.end_date - self.booking.start_date).days
        return total_days >= 1

    def _finalize_booking(self):
        total_days = (self.booking.end_date - self.booking.start_date).days
        self.booking.total_price = self.car.rental_price * total_days
        self.booking.status = 'pending'
        self.booking.save()
        self.request.session['booking_id'] = self.booking.id
