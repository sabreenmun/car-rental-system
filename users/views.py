from .models import*
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cars.models import Car, Booking, Rental 
from notifications.models import  Review
from designpatterns.cors import SecurityQuestion1Handler, SecurityQuestion2Handler, SecurityQuestion3Handler


def car_renter_register(request):
    if request.method == "POST":
        form = CarRenterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = False 
            user.user_type = 'renter'  
            user.save()

            car_renter = CarRenter(
                user=user,
                security_question_1=form.cleaned_data['security_question_1'],
                security_answer_1=form.cleaned_data['security_answer_1'],
                security_question_2=form.cleaned_data['security_question_2'],
                security_answer_2=form.cleaned_data['security_answer_2'],
                security_question_3=form.cleaned_data['security_question_3'],
                security_answer_3=form.cleaned_data['security_answer_3'],
            )
            car_renter.save()

            return redirect('car_renter_login')
    else:
        form = CarRenterRegistrationForm()
    
    return render(request, 'users/car_renter_register.html', {'form': form})



def car_renter_login(request):
    if request.method == "POST":
        form = CarRenterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_superuser:
                login(request, user)
                return redirect('car_list')
    else:
        form = CarRenterLoginForm()
    return render(request, 'users/car_renter_login.html', {'form': form})


def request_password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username, is_superuser=False).first()
            if user:
                request.session['reset_user_id'] = user.id
                return redirect('car_renter_verify_security_questions')
    else:
        form = PasswordResetForm()
    return render(request, 'users/request_password_reset.html', {'form': form})


def verify_security_questions(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('request_password_reset')
    
    user = get_object_or_404(User, id=user_id)

    # You can assume the user is a renter here
    car_renter = get_object_or_404(CarRenter, user=user)

    # Create the chain of responsibility
    handler1 = SecurityQuestion1Handler()
    handler2 = SecurityQuestion2Handler(handler1)
    handler3 = SecurityQuestion3Handler(handler2)

    if request.method == "POST":
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            # retrieve answers and question number from the form
            security_answer_1 = form.cleaned_data['security_answer_1']
            security_answer_2 = form.cleaned_data['security_answer_2']
            security_answer_3 = form.cleaned_data['security_answer_3']

            # verify answers through the chain of responsibility
            if (handler3.handle(car_renter, security_answer_1, 1) and
                handler3.handle(car_renter, security_answer_2, 2) and
                handler3.handle(car_renter, security_answer_3, 3)):
                
                request.session['security_verified'] = True
                return redirect('car_renter_set_new_password')
            else:
                # optionally, you can add a message for incorrect answers
                form.add_error(None, 'One or more answers are incorrect.')
    else:
        form = SecurityQuestionForm()

    return render(request, 'users/verify_security_questions.html', {'form': form})


def set_new_password(request):
    if not request.session.get('security_verified'):
        return redirect('request_password_reset')
    user_id = request.session.get('reset_user_id')
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return redirect('car_renter_login')
    else:
        form = SetNewPasswordForm()
    return render(request, 'users/set_new_password.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    cars = None
    bookings = None
    rentals = None
    reviews = None  # Initialize the reviews variable

    if user.is_superuser:  # Car Owner
        cars = Car.objects.filter(owner=user)
        rentals = Rental.objects.filter(car_owner=user)  # Owner's rental history
        reviews = Review.objects.filter(reviewed_user=user)  # Reviews for the car owner
    else:  # Car Renter
        bookings = Booking.objects.filter(renter=user)
        rentals = Rental.objects.filter(renter=user)  # Renter's rental history
        reviews = Review.objects.filter(reviewer=user)  # Reviews given by this renter

    return render(request, "users/profile.html", {
        "user": user,
        "cars": cars,
        "bookings": bookings,
        "rentals": rentals,
        "reviews": reviews,
    })

def user_logout(request):
    
    if request.user.is_superuser:
        logout(request)  
        return redirect("car_owner_login")  
    else:
        logout(request)  
        return redirect("login")
