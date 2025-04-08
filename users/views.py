from .models import*
from .forms import *
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from notifications.models import  Review
from designpatterns.cors import SecurityQuestion1Handler, SecurityQuestion2Handler, SecurityQuestion3Handler
from designpatterns.singleton import Singleton
from django.utils import timezone
from django.contrib import messages
from cars.models import Car, Booking
from django.contrib.messages import get_messages
User = get_user_model()

#method to register as a car renter
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

#method to login as a car renter
def car_renter_login(request):
    get_messages(request).used = True
    if request.method == "POST":
        form = CarRenterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #authenticate the user with provided credentials
            user = authenticate(request, username=username, password=password)
            
            if user is not None and not user.is_superuser:
                session_manager = Singleton()   #get singleton instance
                session_manager.login_user(request, user)  #log user in using singleton
                return redirect('car_list')
            else:
                #invalid creds
                messages.error(request, 'Invalid credentials for a car renter.')
        else:
            #if form validation fails
            messages.error(request, 'There was an error with your login form.')
    else:
        form = CarRenterLoginForm()

    return render(request, 'users/car_renter_login.html', {'form': form})

#method to request a pass reset for car renter
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
                #add error message
                messages.error(request, "Invalid username!")
    else:
        form = PasswordResetForm()

    return render(request, 'users/request_password_reset.html', {'form': form})

#method for verification for car renters.
def verify_security_questions(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('request_password_reset')
    
    user = get_object_or_404(User, id=user_id)

    #assume user is a renter
    car_renter = get_object_or_404(CarRenter, user=user)

    #create the chain of responsibilities
    handler1 = SecurityQuestion1Handler()
    handler2 = SecurityQuestion2Handler()
    handler3 = SecurityQuestion3Handler()

    #set successors for future handling
    handler1.set_successor(handler2)
    handler2.set_successor(handler3)

    if request.method == "POST":
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            # retrieve answers and question number from the form
            security_answer_1 = form.cleaned_data['security_answer_1']
            security_answer_2 = form.cleaned_data['security_answer_2']
            security_answer_3 = form.cleaned_data['security_answer_3']

            # verify answers through the chain of responsibility
            if (handler1.handle_request(car_renter, security_answer_1, 1) and
                handler1.handle_request(car_renter, security_answer_2, 2) and
                handler1.handle_request(car_renter, security_answer_3, 3)):
                
                request.session['security_verified'] = True
                return redirect('car_renter_set_new_password')
            else:
                form.add_error(None, 'One or more of your answers are incorrect. Please try again.')
    else:
        form = SecurityQuestionForm()

    # make sure a response is returned in all cases
    return render(request, 'users/verify_security_questions.html', {'form': form})

#method to set new pass for car renter
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
                 form.add_error('confirm_password', 'Passwords do not match!') 
    else:
        form = SetNewPasswordForm()
    return render(request, 'users/set_new_password.html', {'form': form})

#method to view profile for car renter
@login_required
def profile(request):
    user = request.user
    cars = None
    bookings = None
    reviews = None 

    #todays date
    today = timezone.now().date()

    #for the car owner
    if user.is_superuser:  
        cars = Car.objects.filter(owner=user)
        reviews = Review.objects.filter(reviewed_user=user) 
        
        for car in cars:
            car.past_bookings = Booking.objects.filter(car=car, end_date__lt=today)

    else:  #for the car Renter
        bookings = Booking.objects.filter(renter=user, end_date__lt=today) 
        reviews = Review.objects.filter(reviewer=user)


    return render(request, "users/profile.html", {
        "user": user,
        "cars": cars,
        "bookings": bookings,
        "reviews": reviews,
    })


#method to logout all users
def user_logout(request):
    
    if request.user.is_superuser:
        logout(request)  
        return redirect("car_owner_login")  
    else:
        logout(request)  
        return redirect("login")
