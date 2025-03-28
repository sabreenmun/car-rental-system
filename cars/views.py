from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Car, Booking
from notifications.models import Notification
import random
from designpatterns.carbuilder import CarBuilder
from designpatterns.proxy import PaymentGatewayProxy
from django.db.models import Q 

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
    booked_renters = Booking.objects.filter(is_confirmed=True).values_list("renter", flat=True)

    return render(request, "cars/car_list.html", {"cars": cars, "booked_cars": booked_cars})


@login_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            # Using the CarBuilder
            builder = CarBuilder()
            
            # Prepare dates from form if they exist
            available_from = form.cleaned_data['available_from'] if form.cleaned_data.get('available_from') else None
            available_to = form.cleaned_data['available_to'] if form.cleaned_data.get('available_to') else None

            # Build the car object using the builder
            car = (builder
                   .set_owner(request.user)
                   .set_model(form.cleaned_data['model'])
                   .set_image(form.cleaned_data['image'])
                   .set_year(form.cleaned_data['year'])
                   .set_mileage(form.cleaned_data['mileage'])
                   .set_pickup_location(form.cleaned_data['pickup_location'])
                   .set_rental_price(form.cleaned_data['rental_price'])
                   .set_available_dates(available_from, available_to)  # Using available_from and available_to
                   .build())
            
            # Save the car instance
            car.save()

            return redirect("car_list")  # Redirect to car list view after successful creation
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
        """ Ensure the image and new availability fields are updated correctly """
        car = self.get_object()
        
        # Handle image update
        if self.request.FILES.get('image'):  
            car.image = self.request.FILES['image']
        
        # Handle the other fields
        car.model = form.cleaned_data['model']
        car.year = form.cleaned_data['year']
        car.mileage = form.cleaned_data['mileage']
        car.pickup_location = form.cleaned_data['pickup_location']
        car.rental_price = form.cleaned_data['rental_price']
        car.available_from = form.cleaned_data['available_from']
        car.available_to = form.cleaned_data['available_to']
        
        # Save the updated car
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

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create booking object, but don't save yet
            booking = form.save(commit=False)
            booking.car = car
            booking.renter = request.user

            # Check if requested dates fall within car's available period
            if not (car.available_from <= booking.start_date and car.available_to >= booking.end_date):
                messages.error(request, "Selected dates are outside the car's availability range.")
                return render(request, "cars/book_car.html", {"form": form, "car": car})

            # Check for conflicting bookings
            conflicting_bookings = Booking.objects.filter(
                car=car, is_confirmed=True
            ).filter(
                Q(start_date__lt=booking.end_date) & Q(end_date__gt=booking.start_date)
            )

            if conflicting_bookings.exists():
                messages.error(request, "This car is already booked for the selected dates.")
                return render(request, "cars/book_car.html", {"form": form, "car": car})

            # Ensure at least 1 full day is selected
            total_days = (booking.end_date - booking.start_date).days
            if total_days < 1:
                messages.error(request, "End date must be after start date.")
                return render(request, "cars/book_car.html", {"form": form, "car": car})

            # Calculate total price
            booking.total_price = car.rental_price * total_days
            # Set the booking status to pending (not confirmed)
            booking.status = 'pending'  # or a similar status that denotes payment is needed

            # Save booking to the database with status as pending
            booking.save()

            # Store the booking ID temporarily in session for payment processing
            request.session['booking_id'] = booking.id

            messages.success(request, "Booking successful! Proceed to payment.")
            return redirect("process_payment", booking.id)

    else:
        form = BookingForm()

    return render(request, "cars/book_car.html", {"form": form, "car": car})

@login_required
def process_payment(request, booking_id):
    # Retrieve the booking data from the session
    booking = get_object_or_404(Booking, id=booking_id)

    total_days = booking.total_price / booking.car.rental_price
    
      # Check if the booking is unconfirmed and there are date conflicts
    if not booking.is_confirmed:
        # Check for date conflicts with other confirmed bookings for the same car
        conflicting_bookings = Booking.objects.filter(
            car=booking.car,
            is_confirmed=True,
            start_date__lt=booking.end_date,
            end_date__gt=booking.start_date
        )

        if conflicting_bookings.exists():
            # Redirect to the update booking page if there's a conflict
            return redirect('update_booking', booking_id=booking.id)

        
    if request.method == "POST":
        # Use the PaymentGatewayProxy to handle payment processing
        payment_gateway = PaymentGatewayProxy()
        payment_result = payment_gateway.process_payment(booking.total_price, request.user)

        success = payment_result["status"] == "completed"
        transaction_id = payment_result["transaction_id"]

        # Create the payment record
        payment = Payment.objects.create(
            booking=booking,
            renter=request.user,
            amount=booking.total_price,
            status="completed" if success else "failed",
            transaction_id=transaction_id,
        ) 

        # If payment is successful, confirm the booking
        if success:
            booking.is_confirmed = True  # Confirm booking after successful payment
            booking.save()
            messages.success(request, f"Payment successful! You have paid ${booking.total_price}. Your booking is confirmed.")
        else:
            # If payment failed, do not confirm the booking
            booking.is_confirmed = False  # Ensure booking remains unconfirmed
            booking.save()
            messages.error(request, "Payment failed! Please try again.")

        # Redirect to payment status page to show payment result
        return redirect("payment_status", booking.id)

    # Render the payment page if the method is GET
     # Render the payment page if the method is GET
    return render(request, "cars/payment.html", {
        "booking": booking,
        "total_days": total_days  # Pass total_days to the template
    })


@login_required
def payment_status(request, booking_id):
    # Retrieve the booking and associated payment information
    booking = get_object_or_404(Booking, id=booking_id)
    payment = Payment.objects.filter(booking=booking).first()  # Get the first payment related to this booking

    # Inform the user if the booking is not confirmed yet
    if not booking.is_confirmed:
        messages.info(request, "Your booking is not confirmed yet. Please complete the payment to confirm your booking.")

    # Render the payment status page with the booking and payment information
    return render(request, "cars/payment_status.html", {"booking": booking, "payment": payment})


@login_required
def my_bookings(request):
    # Filter bookings for the logged-in user
    bookings = Booking.objects.filter(renter=request.user)
    
    return render(request, "cars/my_bookings.html", {"bookings": bookings})

@login_required
def car_search(request):
    form = CarSearchForm(request.GET)
    cars = Car.objects.all()

    if form.is_valid():
        model = form.cleaned_data.get('model')
        rental_price_min = form.cleaned_data.get('rental_price_min')
        rental_price_max = form.cleaned_data.get('rental_price_max')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')

        # Filter based on model and price range
        if model:
            cars = cars.filter(model__icontains=model)
        if rental_price_min:
            cars = cars.filter(rental_price__gte=rental_price_min)
        if rental_price_max:
            cars = cars.filter(rental_price__lte=rental_price_max)

        # Filter cars based on availability for the selected date range
        if from_date and to_date:
            available_cars = []
            for car in cars:
                # Check if the car is available for the selected date range
                if car.is_available(from_date, to_date):
                    # Check for any existing bookings that conflict with the requested dates
                    conflicting_bookings = Booking.objects.filter(car=car, is_confirmed=True)
                    available = True
                    for booking in conflicting_bookings:
                        if (from_date <= booking.end_date) and (to_date >= booking.start_date):
                            available = False
                            break
                    
                    if available:
                        available_cars.append(car)

            # Update the cars queryset to only include available cars
            cars = Car.objects.filter(id__in=[car.id for car in available_cars])

    return render(request, "cars/car_search.html", {"form": form, "cars": cars})

@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Get the new start and end dates from the form
        new_start_date = request.POST.get('start_date')
        new_end_date = request.POST.get('end_date')

        try:
            # Convert string dates to datetime objects
            new_start_date = datetime.strptime(new_start_date, '%Y-%m-%d')
            new_end_date = datetime.strptime(new_end_date, '%Y-%m-%d')

            # Ensure start date is before end date
            if new_start_date >= new_end_date:
                messages.error(request, "Start date cannot be after or the same as the end date. Please choose valid dates.")
                return render(request, 'cars/update_booking.html', {'booking': booking})

        except ValueError:
            messages.error(request, "Invalid date format. Please choose valid dates.")
            return render(request, 'cars/update_booking.html', {'booking': booking})

        # Check for date conflicts with confirmed bookings
        conflicting_bookings = Booking.objects.filter(
            car=booking.car,
            is_confirmed=True,
            start_date__lt=new_end_date,
            end_date__gt=new_start_date
        )

        if conflicting_bookings.exists():
            messages.error(request, "The selected dates conflict with another confirmed booking. Please choose different dates.")
            return render(request, 'cars/update_booking.html', {'booking': booking})

        # Update the booking dates if no conflicts
        booking.start_date = new_start_date
        booking.end_date = new_end_date

        # Calculate the total days and total cost based on the new booking dates
        total_days = (new_end_date - new_start_date).days
        if total_days < 0:
            total_days = 0  # If there's an issue with the calculation, ensure it's a positive number.

        # Assuming 'daily_rate' is a field in your 'Car' model
        total_price = total_days * booking.car.rental_price  # Adjust this calculation as needed.

        # Update the booking with the new total days and total price
        booking.total_days = total_days
        booking.total_price = total_price

        # Save the updated booking
        booking.save()

        # If the booking is unconfirmed, redirect to the payment page for confirmation
        if not booking.is_confirmed:
            messages.success(request, "Booking dates updated! Proceed to payment to confirm your booking.")
            return redirect("process_payment", booking_id=booking.id)

        messages.success(request, "Your booking dates have been successfully updated!")
        return redirect('my_bookings')

    # Render the page to update booking dates
    return render(request, 'cars/update_booking.html', {'booking': booking})

@login_required
def booking_delete(request, booking_id):
    # Get the booking object by ID or 404 if not found
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if the current user is either the car owner or the renter
    if booking.car.owner == request.user:
        # If the user is the car owner, allow deletion
        user_role = "owner"
    elif booking.renter == request.user:
        # If the user is the renter, allow deletion
        user_role = "renter"
    else:
        # If the user is neither the car owner nor the renter, deny access
        messages.error(request, "You are not authorized to delete this booking.")
        return redirect("bookings_page")  # Redirect to bookings page if unauthorized

    if request.method == "POST":
        # Delete the booking if it's a POST request
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect("bookings_page")  # Redirect to bookings page after deletion

    return render(request, "booking/booking_confirm_delete.html", {"booking": booking, "user_role": user_role})

@login_required
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    car = booking.car  # Get the associated car
    
    # Delete the booking
    booking.delete()
    
    # Redirect to the car detail page using pk (the car's id)
    return redirect(reverse('car_detail', kwargs={'pk': car.id}))