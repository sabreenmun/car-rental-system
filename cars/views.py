from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Car, Booking
from notifications.models import Notification
import random


@login_required
def car_list(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:  
            cars = Car.objects.filter(owner=request.user)  
        else:  
            cars = Car.objects.all()  
    else:
        cars = Car.objects.none()  

    booked_cars = Booking.objects.filter(is_confirmed=True).values_list("car_id", flat=True) 

    return render(request, "cars/car_list.html", {"cars": cars, "booked_cars": booked_cars})


@login_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES) 
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect("car_list")
    else:
        form = CarForm()
    return render(request, "cars/car_form.html", {"form": form})


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'cars/car_update.html'

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        car = get_object_or_404(Car, pk=self.kwargs['pk'])
        if car.owner != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this car.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """ Ensure the image is updated correctly """
        car = self.get_object() 
        if self.request.FILES.get('image'):  
            car.image = self.request.FILES['image']
        car.model = form.cleaned_data['model']
        car.year = form.cleaned_data['year']
        car.mileage = form.cleaned_data['mileage']
        car.availability = form.cleaned_data['availability']
        car.pickup_location = form.cleaned_data['pickup_location']
        car.rental_price = form.cleaned_data['rental_price']
        car.save()  

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('car_list')


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()

  
        booking = Booking.objects.filter(car=car).first()  
        context['booking'] = booking 

        return context 


@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)

   
    if car.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this car.")

    if request.method == "POST":
        car.delete()
        return redirect("car_list")

    return render(request, "cars/car_confirm_delete.html", {"car": car})

from datetime import timedelta

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)  # form থেকে instance তৈরি, কিন্তু এখনো save করিনি
            booking.car = car  # ForeignKey সেট করলাম
            booking.renter = request.user  # যে ইউজার বুকিং করছে

            # **Ensure the car is set before accessing it**
            if not booking.car:
                messages.error(request, "Car information is missing.")
                return redirect("cars:car_list")  # অথবা অন্য পেজে রিডাইরেক্ট করো

            # **Check for conflicting bookings**
            if booking.is_conflicting():
                messages.error(request, "This car is already booked for the selected dates.")
            else:
                # **Calculate total price**: Ensure at least 1 day is selected
                total_days = (booking.end_date - booking.start_date).days
                if total_days < 1:
                    messages.error(request, "End date must be after start date.")
                    return redirect("cars:car_list")
                
                booking.total_price = car.rental_price * total_days
                booking.save()  # save the booking instance

                # **Update car availability**: Remove booked dates from car's available dates
                booked_dates = car.get_date_range(booking.start_date, booking.end_date)
                car.available_dates = list(set(car.available_dates) - set(booked_dates))
                car.save()

                # **Debugging output to ensure booking is created**
                print(f"Booking for Car: {booking.car} by {booking.renter} from {booking.start_date} to {booking.end_date}")

                # **Redirect to payment processing page**
                return redirect("process_payment", booking.id)

    else:
        form = BookingForm()

    return render(request, "cars/book_car.html", {"form": form, "car": car})

@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        payment_gateway = PaymentGatewayProxy()
        payment_result = payment_gateway.process_payment(booking.total_price, request.user)

        success = payment_result["status"] == "completed"
        transaction_id = payment_result["transaction_id"]

        payment = Payment.objects.create(
            booking=booking,
            renter=request.user,
            amount=booking.total_price,
            status="completed" if success else "failed",
            transaction_id=transaction_id,
        )

        if success:
            booking.is_confirmed = True
            booking.save()
            messages.success(request, f"Payment successful! You have paid ${booking.total_price}. Your booking is confirmed.")
        else:
            messages.error(request, "Payment failed! Please try again.")

        return redirect("payment_status", booking.id)

    return render(request, "cars/payment.html", {"booking": booking})


@login_required
def payment_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = booking.payment if hasattr(booking, 'payment') else None

    return render(request, "cars/payment_status.html", {"booking": booking, "payment": payment})


class PaymentGatewayProxy:
    def process_payment(self, amount, user):
       
        success = True  
        transaction_id = f"TXN{random.randint(10000, 99999)}"  
        
        if success:
            return {"status": "completed", "transaction_id": transaction_id}
        else:
            return {"status": "failed", "transaction_id": transaction_id}
        


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(renter=request.user)
    
    return render(request, "cars/my_bookings.html", {"bookings": bookings})


@login_required
def car_search(request):
    form = CarSearchForm(request.GET)
    cars = Car.objects.all()

    
    booked_cars = Booking.objects.filter(is_confirmed=True).values_list("car_id", flat=True)

    if form.is_valid():
        model = form.cleaned_data.get('model')
        rental_price_min = form.cleaned_data.get('rental_price_min')
        rental_price_max = form.cleaned_data.get('rental_price_max')

        if model:
            cars = cars.filter(model__icontains=model) 
        if rental_price_min:
            cars = cars.filter(rental_price__gte=rental_price_min)
        if rental_price_max:
            cars = cars.filter(rental_price__lte=rental_price_max)

    
    if request.user.is_superuser:  
        cars = cars.filter(owner=request.user)

    return render(request, "cars/car_search.html", {"form": form, "cars": cars, "booked_cars": booked_cars})