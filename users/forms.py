from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarRenter, CustomUser
from django.contrib.auth import get_user_model
from django import forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

#form to register as car renter
class CarRenterRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    #initialize securuty questions
    SECURITY_QUESTIONS = [
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("What city were you born in?", "What city were you born in?"),
        ("What was the name of your elementary school?", "What was the name of your elementary school?"),
    ]
    
    security_question_1 = forms.CharField(initial=SECURITY_QUESTIONS[0][1], widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    security_answer_1 = forms.CharField(widget=forms.PasswordInput)
    security_question_2 = forms.CharField(initial=SECURITY_QUESTIONS[1][1], widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    security_answer_2 = forms.CharField(widget=forms.PasswordInput)
    security_question_3 = forms.CharField(initial=SECURITY_QUESTIONS[2][1], widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    security_answer_3 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

#save user w new data
def save(self, commit=True):
    
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password'])
    if commit:
        user.save() 
    
   #register car user with user, email, pass + questions and answers
    car_renter = CarRenter(  
        user=user,  
        security_question_1=self.cleaned_data['security_question_1'],
        security_answer_1=self.cleaned_data['security_answer_1'],
        security_question_2=self.cleaned_data['security_question_2'],
        security_answer_2=self.cleaned_data['security_answer_2'],
        security_question_3=self.cleaned_data['security_question_3'],
        security_answer_3=self.cleaned_data['security_answer_3']
    )

    if commit:
        car_renter.save()
    
    return user

#form to login as renter
class CarRenterLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#form to reset password for renter
class PasswordResetForm(forms.Form):
    username = forms.CharField()

#form to answer security quesitons for renter
class SecurityQuestionForm(forms.Form):
    security_answer_1 = forms.CharField(label="What is your mother's maiden name?", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'}))
    security_answer_2 = forms.CharField(label="What city were you born in?", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'}))
    security_answer_3 = forms.CharField(label="What was the name of your elementary school?", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'}))

#form to set new password
class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)