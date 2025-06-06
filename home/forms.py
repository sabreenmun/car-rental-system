from django import forms
from django.contrib.auth import get_user_model
from .models import CarOwner


User = get_user_model()

#form for car owner registraiton
class CarOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    #initialize security questions
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
        model = User  
        fields = ['username', 'email', 'password']

def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password'])
    if commit:
        user.save()
   
   #save the car owner with the 3 questions and answers, along w sending their user,email,and pass into the new model that they are.
    car_renter = CarOwner(  
        user=user,
        security_question_1=self.cleaned_data['security_question_1'],
        security_answer_1=self.cleaned_data['security_answer_1'],
        security_question_2=self.cleaned_data['security_question_2'],
        security_answer_2=self.cleaned_data['security_answer_2'],
        security_question_3=self.cleaned_data['security_question_3'],
        security_answer_3=self.cleaned_data['security_answer_3']
    )
    car_renter.save()
    return user

#form for car owner to login
class CarOwnerLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#form to reset pass for car owners
class PasswordResetForm(forms.Form):
    username = forms.CharField()

#form to answer 3 security questions
class SecurityQuestionForm(forms.Form):
    security_answer_1 = forms.CharField(
        label="What is your mother's maiden name?",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )
    security_answer_2 = forms.CharField(
        label="What city were you born in?",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )
    security_answer_3 = forms.CharField(
        label="What was the name of your elementary school?",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )

#form to set new pass
class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

#form to choose login choice
class LoginChoiceForm(forms.Form):
    USER_CHOICES = [
        ('car_owner', 'Car Owner'),
        ('car_renter', 'Car Renter'),
    ]
    user_type = forms.ChoiceField(choices=USER_CHOICES, widget=forms.RadioSelect, label="Select your login type:")
