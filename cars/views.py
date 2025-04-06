from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Car, Booking
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from notifications.models import Notification
import random
from designpatterns.carbuilder import CarBuilder, CarDirector, ConcreteCarBuilder
from designpatterns.proxy import Client
from django.db.models import Q 
from notifications.models import Review
from designpatterns.mediator import *

#method to view car list
@login_required
def car_list(request):
    #if user is owner/superuser, filter listings to owned cars
    if request.user.is_authenticated:
        if request.user.is_superuser:  
            cars = Car.objects.filter(owner=request.user)  
        else:  
            cars = Car.objects.all()  
    else:
        cars = Car.objects.none()  

    booked_cars = Booking.objects.filter(is_confirmed=True).values_list("car_id", flat=True) 
    booked_renters = Booking.objects.filter(is_confirmed=True).values_list("renter", flat=True)

    return render(request, "cars/car_list.html", {"cars": cars, "booked_cars": booked_cars})

#method to post a car listing
@login_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            
            #instantiate the concretebuilder
            car = ConcreteCarBuilder()

            #instantiate the director (hire the engineer)
            director = CarDirector(car)
  
            #prepare dates from form if they exist
            available_from = form.cleaned_data['available_from'] if form.cleaned_data.get('available_from') else None
            available_to = form.cleaned_data['available_to'] if form.cleaned_data.get('available_to') else None
           
            #use the Director to build the car
            car = director.construct_car(
                owner=request.user,
                model=form.cleaned_data['model'],
                image=form.cleaned_data['image'],
                year=form.cleaned_data['year'],
                mileage=form.cleaned_data['mileage'],
                pickup_location=form.cleaned_data['pickup_location'],
                rental_price=form.cleaned_data['rental_price'],
                available_from=available_from,
                available_to=available_to
            )
            
            #save the car instance
            car.save()

            return redirect("car_list")  #redirect to car list view after successful creation
    else:
        form = CarForm()

    return render(request, "cars/car_form.html", {"form": form})


#method to update a listing
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
        car = self.get_object()
        
        #handle image update
        if self.request.FILES.get('image'):  
            car.image = self.request.FILES['image']
        
        #handle the other field updates
        car.model = form.cleaned_data['model']
        car.year = form.cleaned_data['year']
        car.mileage = form.cleaned_data['mileage']
        car.pickup_location = form.cleaned_data['pickup_location']
        car.rental_price = form.cleaned_data['rental_price']
        car.available_from = form.cleaned_data['available_from']
        car.available_to = form.cleaned_data['available_to']
        
        #save the updated car
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

        today = date.today()  #today's date

        #get the first booking related to the car
        booking = Booking.objects.filter(car=car).first()  
        context['booking'] = booking

        #pass today's date to the context
        context['today'] = today

        #get all reviews related to the car
        reviews = Review.objects.filter(car=car)
        context['reviews'] = reviews

        return context

#method to delete a car listing
@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this car.")

    if request.method == "POST":
        car.delete()
        return redirect("car_list")

    return render(request, "cars/car_confirm_delete.html", {"car": car})

#method to book a car
@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            #create booking object, but don't save yet
            booking = form.save(commit=False)
            booking.car = car
            booking.renter = request.user

            #check if requested dates fall within car's available period
            if not (car.available_from <= booking.start_date and car.available_to >= booking.end_date):
                messages.error(request, "Selected dates are outside the car's availability range.")
                return render(request, "cars/book_car.html", {"form": form, "car": car})

            #check for conflicting bookings
            conflicting_bookings = Booking.objects.filter(
                car=car, is_confirmed=True
            ).filter(
                Q(start_date__lt=booking.end_date) & Q(end_date__gt=booking.start_date)
            )

            if conflicting_bookings.exists():
                messages.error(request, "This car is already booked for the selected dates.")
                return render(request, "cars/book_car.html", {"form": form, "car": car})

            #ensure at least 1 full day is selected
            total_days = (booking.end_date - booking.start_date).days
            if total_days < 1:
                messages.error(request, "End date must be after start date.")
                return render(request, "cars/book_car.html", {"form": form, "car": car})

            #calculate total price
            booking.total_price = car.rental_price * total_days
            #set the booking status to pending (not confirmed)
            booking.status = 'pending'  # or a similar status that denotes payment is needed

            #save booking to the database with status as pending
            booking.save()

            #store the booking ID temporarily in session for payment processing
            request.session['booking_id'] = booking.id
            return redirect("process_payment", booking.id)

    else:
        form = BookingForm()

    return render(request, "cars/book_car.html", {"form": form, "car": car})

@login_required
def process_payment(request, booking_id):
    #get booking data from the current session
    booking = get_object_or_404(Booking, id=booking_id)
    #calculate cost
    total_days = booking.total_price / booking.car.rental_price
    
    #check if the booking is unconfirmed and there are date conflicts
    if not booking.is_confirmed:
        #check for date conflicts with other confirmed bookings for the same car
        conflicting_bookings = Booking.objects.filter(
            car=booking.car,
            is_confirmed=True,
            start_date__lt=booking.end_date,
            end_date__gt=booking.start_date
        )

        if conflicting_bookings.exists():
            #redirect to the update booking page if there's a conflict
            return redirect('update_booking', booking_id=booking.id)

        
    if request.method == "POST":
        #use the client to handle payment processing
        client = Client()
        success = client.pay_for_booking(booking.total_price, request.user)

       #mock transaction ID
        transaction_id = f"TXN{random.randint(10000, 99999)}"
        
        #create the payment record
        payment = Payment.objects.create(
            booking=booking,
            renter=request.user,
            amount=booking.total_price,
            status="completed" if success else "failed",
            transaction_id=transaction_id,
        )
        #if payment is successful, confirm booking
        if success:
            booking.is_confirmed = True
            booking.save()
            messages.success(request, f"Payment successful! You have paid ${booking.total_price}. Your booking is confirmed.")
        else:
            #if payment failed, do not confirm booking
            booking.is_confirmed = False
            booking.save()
            messages.error(request, "Payment failed! Please try again.")

        #redirect to payment status page to show payment result
        return redirect("payment_status", booking.id)

    #render payment page if the method is GET
    return render(request, "cars/payment.html", {
        "booking": booking,
        "total_days": total_days  #pass total_days to the template
    })


@login_required
def payment_status(request, booking_id):
    #retrieve the booking and associated payment information
    booking = get_object_or_404(Booking, id=booking_id)
    payment = Payment.objects.filter(booking=booking).first()  # Get the first payment related to this booking

    #let the user know if the booking is not confirmed yet
    if not booking.is_confirmed:
        messages.info(request, "Your booking is not confirmed yet. Please complete the payment to confirm your booking.")

    #render the payment status page with the booking and payment information
    return render(request, "cars/payment_status.html", {"booking": booking, "payment": payment})


#method to view my bookings (renters)
@login_required
def my_bookings(request):
    #filter bookings for the logged-in user
    bookings = Booking.objects.filter(renter=request.user)

    #pass today's date to the template
    return render(request, "cars/my_bookings.html", {
        "bookings": bookings,
        "today": date.today()  #pass today's date to compare with booking end dates
    })

#method to search car basedo n conditions
@login_required
def car_search(request):
    form = CarSearchForm(request.GET)
    cars = Car.objects.all()

    # form validation
    if form.is_valid():
        model = form.cleaned_data.get('model')
        rental_price_min = form.cleaned_data.get('rental_price_min')
        rental_price_max = form.cleaned_data.get('rental_price_max')
        available_from = form.cleaned_data.get('available_from')
        available_to = form.cleaned_data.get('available_to')

        #validate rental price range
        if rental_price_min and rental_price_max and rental_price_min > rental_price_max:
            form.add_error('rental_price_max', 'Max rental price cannot be less than min rental price.')

        #validate the date range
        if available_from and available_to and available_from > available_to:
            form.add_error('available_to', 'Available to date cannot be before available from date.')

        #if there are any errors, render it without applying any filters
        if form.errors:
            return render(request, "cars/car_search.html", {"form": form, "cars": cars})

        #filter based on model, price, and dates
        if model:
            cars = cars.filter(model__icontains=model)
        if rental_price_min:
            cars = cars.filter(rental_price__gte=rental_price_min)
        if rental_price_max:
            cars = cars.filter(rental_price__lte=rental_price_max)

        #based on availability dates
        if available_from and available_to:
            available_cars = []
            for car in cars:
                if car.is_available(available_from, available_to):
                    conflicting_bookings = Booking.objects.filter(car=car, is_confirmed=True)
                    available = True
                    for booking in conflicting_bookings:
                        #if another car booked it
                        if available_from <= booking.end_date and available_to >= booking.start_date:
                            available = False
                            break
                    if available:
                        available_cars.append(car)

            #update car set
            cars = cars.filter(id__in=[car.id for car in available_cars])

    return render(request, "cars/car_search.html", {"form": form, "cars": cars})



#method to update a car booking for owners
@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        #get the new start and end dates from the form
        new_start_date = request.POST.get('start_date')
        new_end_date = request.POST.get('end_date')

        try:
            #convert string dates to datetime objects
            new_start_date = datetime.strptime(new_start_date, '%Y-%m-%d')
            new_end_date = datetime.strptime(new_end_date, '%Y-%m-%d')

            #ensure start date is before end date
            if new_start_date >= new_end_date:
                messages.error(request, "Start date cannot be after or the same as the end date. Please choose valid dates.")
                return render(request, 'cars/update_booking.html', {'booking': booking})

        except ValueError:
            messages.error(request, "Invalid date format. Please choose valid dates.")
            return render(request, 'cars/update_booking.html', {'booking': booking})

        #check for date conflicts with confirmed bookings
        conflicting_bookings = Booking.objects.filter(
            car=booking.car,
            is_confirmed=True,
            start_date__lt=new_end_date,
            end_date__gt=new_start_date
        )

        if conflicting_bookings.exists():
            messages.error(request, "The selected dates overlap with another confirmed booking. Please choose different dates.")
            return render(request, 'cars/update_booking.html', {'booking': booking})

        #update the booking dates if no conflicts
        booking.start_date = new_start_date
        booking.end_date = new_end_date

        #calculate the total days and total cost based on the new booking dates
        total_days = (new_end_date - new_start_date).days
        if total_days < 0:
            total_days = 0  # if there's an issue with the calculation, ensure it's a positive number.

        total_price = total_days * booking.car.rental_price

        #update the booking with the new total days and total price
        booking.total_days = total_days
        booking.total_price = total_price

        #save the updated booking
        booking.save()

        #if the booking is unconfirmed, redirect to the payment page for confirmation
        if not booking.is_confirmed:
            messages.success(request, "Booking dates updated! Proceed to payment to confirm your booking.")
            return redirect("process_payment", booking_id=booking.id)

        messages.success(request, "Your booking dates have been successfully updated!")
        return redirect('my_bookings')

    #render the page to update booking dates
    return render(request, 'cars/update_booking.html', {'booking': booking})


#for car owners/renters to delete a booking
@login_required
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    car = booking.car  #get the associated car
    
    today = date.today()
    if booking.start_date <= today <= booking.end_date or booking.end_date < today:
        return redirect(reverse('car_detail', kwargs={'pk': car.id}))
    
    #check if the user is the car owner or the renter of the booking
    if request.user != car.owner and request.user != booking.renter:
        messages.error(request, "You do not have permission to delete this booking.")
        return redirect(reverse('car_detail', kwargs={'pk': car.id}))
    
    #delete the booking
    booking.delete()

    #if it's the car owner's page, redirect to car_detail page
    if request.user == car.owner:
        return redirect(reverse('car_detail', kwargs={'pk': car.id}))
    
    #if it's the renter's page, redirect to my_bookings page
    return redirect(reverse('my_bookings'))
