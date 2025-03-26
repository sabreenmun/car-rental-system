from django import forms
from django.contrib.auth import get_user_model
from .models import CarOwner


User = get_user_model()


class CarOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

   
    SECURITY_QUESTIONS = [
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("what was the model of your first car?", "what was the model of your first car?"),
        ("What is the name of your first pet?", "What is the name of your first pet?"),
    ]

    # Hardcoded security questions
    security_question_1 = forms.CharField(
        initial=SECURITY_QUESTIONS[0][1],  # Set the first question as default
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # Make it read-only
    )
    security_answer_1 = forms.CharField(widget=forms.PasswordInput)

    security_question_2 = forms.CharField(
        initial=SECURITY_QUESTIONS[1][1],  # Set the second question as default
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # Make it read-only
    )
    security_answer_2 = forms.CharField(widget=forms.PasswordInput)

    security_question_3 = forms.CharField(
        initial=SECURITY_QUESTIONS[2][1],  
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  
    )
    security_answer_3 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User  
        fields = ['username', 'email', 'password']

class CarOwnerLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    username = forms.CharField()

from django import forms

class SecurityQuestionForm(forms.Form):
    security_answer_1 = forms.CharField(
        label="What is your mother's maiden name?",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )
    security_answer_2 = forms.CharField(
        label="What was the model of your first car?",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )
    security_answer_3 = forms.CharField(
        label="What is the name of your first pet?",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


from django import forms

class LoginChoiceForm(forms.Form):
    USER_CHOICES = [
        ('car_owner', 'Car Owner'),
        ('car_renter', 'Car Renter'),
    ]
    user_type = forms.ChoiceField(choices=USER_CHOICES, widget=forms.RadioSelect, label="Select your login type:")
