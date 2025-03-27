from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from cars.models import Rental
from django.http import HttpResponse
from designpatterns.cors import SecurityQuestion1Handler, SecurityQuestion2Handler, SecurityQuestion3Handler
from designpatterns.sessionmanager import SessionManager

User = get_user_model()


def home(request):
    return render(request, 'home/homepage.html')  

def about(request):
    return render(request, 'home/about.html')  

def contact(request):
    return render(request, 'home/contact.html')  

def help(request):
    return render(request, 'home/help.html')



def car_owner_register(request):
    if request.method == "POST":
        form = CarOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = True  
            user.save()

            car_owner = CarOwner(
                user=user,
                security_question_1=form.cleaned_data['security_question_1'],
                security_answer_1=form.cleaned_data['security_answer_1'],
                security_question_2=form.cleaned_data['security_question_2'],
                security_answer_2=form.cleaned_data['security_answer_2'],
                security_question_3=form.cleaned_data['security_question_3'],
                security_answer_3=form.cleaned_data['security_answer_3'],
            )
            car_owner.save()

            return redirect('car_owner_login')

    else:
        form = CarOwnerRegistrationForm()
    
    return render(request, 'home/car_owner_register.html', {'form': form})


def car_owner_login(request):
    if request.method == "POST":
        form = CarOwnerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                session_manager = SessionManager()  # Singleton instance
                session_manager.login_user(request, user)
                return redirect('car_list')  # Redirect to the appropriate page

    else:
        form = CarOwnerLoginForm()

    return render(request, 'home/car_owner_login.html', {'form': form})

def request_password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username, is_superuser=True).first()
            if user:
                request.session['reset_user_id'] = user.id
                return redirect('verify_security_questions')

    else:
        form = PasswordResetForm()

    return render(request, 'home/register_password_reset.html', {'form': form})

def verify_security_questions(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('request_password_reset')

    user = get_object_or_404(User, id=user_id)
    car_owner = get_object_or_404(CarOwner, user=user)

    # Create the chain of responsibility
    handler1 = SecurityQuestion1Handler()
    handler2 = SecurityQuestion2Handler(handler1)
    handler3 = SecurityQuestion3Handler(handler2)

    if request.method == "POST":
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            security_answer_1 = form.cleaned_data['security_answer_1']
            security_answer_2 = form.cleaned_data['security_answer_2']
            security_answer_3 = form.cleaned_data['security_answer_3']

            # Verify answers through the chain of responsibility
            if (handler3.handle(car_owner, security_answer_1, 1) and
                handler3.handle(car_owner, security_answer_2, 2) and
                handler3.handle(car_owner, security_answer_3, 3)):
                
                request.session['security_verified'] = True
                return redirect('set_new_password')
            else:
                form.add_error(None, 'One or more answers are incorrect.')

    else:
        form = SecurityQuestionForm()

    # Ensure a response is returned in all cases
    return render(request, 'home/verify_security_questions.html', {'form': form})


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
                return redirect('car_owner_login')

    else:
        form = SetNewPasswordForm()

    return render(request, 'home/set_new_password.html', {'form': form})



def login_choice(request):
    if request.method == 'POST':
        form = LoginChoiceForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            if user_type == 'car_owner':
                return redirect('car_owner_login')  
            elif user_type == 'car_renter':
                return redirect('car_renter_login')  
    else:
        form = LoginChoiceForm()

    return render(request, 'home/login_choice.html', {'form': form})


def register_choice(request):
    return render(request, 'home/register_choice.html')  

