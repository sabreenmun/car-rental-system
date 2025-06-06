from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.http import HttpResponse
from designpatterns.cors import SecurityQuestion1Handler, SecurityQuestion2Handler, SecurityQuestion3Handler
from designpatterns.singleton import Singleton
from django.contrib.messages import get_messages

User = get_user_model()

#for navigation bar
def home(request):
    return render(request, 'home/homepage.html')  

def about(request):
    return render(request, 'home/about.html')  

def contact(request):
    return render(request, 'home/contact.html')  

def help(request):
    return render(request, 'home/help.html')

#method register a car owner
def car_owner_register(request):
    get_messages(request).used = True
    if request.method == "POST":
        form = CarOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = True  
            user.save()

            #store security questions and user/pass/email from user model
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

#method to allow owners to login
def car_owner_login(request):
    storage = messages.get_messages(request)
    storage.used = True 
    
    if request.method == "POST":
        form = CarOwnerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
             #authenticate the user with provided credentials
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                session_manager = Singleton()  #get singleton instance
                session_manager.login_user(request, user)  #log user in using singleton
        
                return redirect('car_list')
            else:
                #invalid creds
                messages.error(request, 'Invalid credentials for a car owner.')
        else:
            #if form validation fails
            messages.error(request, 'Invalid form submission. Please try again.')

    else:
        form = CarOwnerLoginForm()

    return render(request, 'home/car_owner_login.html', {'form': form})

#method to request a password reset for owners
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
                #add error message
                messages.error(request, "Invalid username!")
    else:
        form = PasswordResetForm()

    return render(request, 'home/register_password_reset.html', {'form': form})

#message to handle the 3 seucirty quesitons
def verify_security_questions(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('request_password_reset')

    user = get_object_or_404(User, id=user_id)
    car_owner = get_object_or_404(CarOwner, user=user)

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
            if (handler1.handle_request(car_owner, security_answer_1, 1) and
                handler1.handle_request(car_owner, security_answer_2, 2) and
                handler1.handle_request(car_owner, security_answer_3, 3)):
                
                request.session['security_verified'] = True
                return redirect('set_new_password')
            else:
                form.add_error(None, 'One or more of your answers are incorrect. Please try again.')

    else:
        form = SecurityQuestionForm()

    # make sure a response is returned in all cases
    return render(request, 'home/verify_security_questions.html', {'form': form})

#method to set new password
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
                 form.add_error('confirm_password', 'Passwords do not match!') 

    else:
        form = SetNewPasswordForm()

    return render(request, 'home/set_new_password.html', {'form': form})


#method to choose login as owner or renter
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

#method to register as car owner or renter
def register_choice(request):
    return render(request, 'home/register_choice.html')  

