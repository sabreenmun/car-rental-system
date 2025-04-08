from django import forms
from .models import *
from datetime import date

#form to post a car with fields required!
class CarForm(forms.ModelForm):
    available_from = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "datepicker", "placeholder": "Select start date"}),
        required=True,
        label="Available From"
    )
    available_to = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "datepicker", "placeholder": "Select end date"}),
        required=True,
        label="Available To"
    )

    #make sure year is between 1900-2099
    #make sure availability is valid
    class Meta:
        model = Car
        fields = ["model", "image", "year", "mileage", "pickup_location", "rental_price", "available_from", "available_to"]
        widgets = {
            "model": forms.TextInput(attrs={"class": "form-control", "placeholder": "Car Model"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control", "min": "1900", "max": "2099", "placeholder": "Year"}),
            "mileage": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Mileage"}),
            "pickup_location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pickup Location"}),
            "rental_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Rental Price"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_to = cleaned_data.get("available_to")

        # validate date range: available_from should not be after available_to
        if available_from and available_to and available_from > available_to:
            self.add_error('available_to', "The 'Available To' date cannot be earlier than the 'Available From' date.")
        
        return cleaned_data

#form to book car
class BookingForm(forms.ModelForm):
    #make sure dates are valid!
    class Meta:
        model = Booking
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Select start date"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Select end date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # make sure that the end date is after the start date
        if start_date and end_date and start_date >= end_date:
            self.add_error('end_date', "The 'End Date' must be later than the 'Start Date'.")
        
        return cleaned_data

#form to search for a car
class CarSearchForm(forms.Form):
    model = forms.CharField(
        required=False,
        max_length=100,
        label="Car Model:",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by Car Model"})
    )
    rental_price_min = forms.DecimalField(
        required=False,
        label="Min Price:",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Min Price"})
    )
    rental_price_max = forms.DecimalField(
        required=False,
        label="Max Price:",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Max Price"})
    )
    available_from = forms.DateField(
        required=False,
        label="Available From:",
        initial=date.today,  #default is today
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    available_to = forms.DateField(
        required=False,
        label="Available To:",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    def clean(self):
        cleaned_data = super().clean()
        rental_price_min = cleaned_data.get('rental_price_min')
        rental_price_max = cleaned_data.get('rental_price_max')
        available_from = cleaned_data.get('available_from')
        available_to = cleaned_data.get('available_to')

        #make sure min price is not greater than max price
        if rental_price_min and rental_price_max and rental_price_min > rental_price_max:
            self.add_error('rental_price_max', "The 'Max Rental Price' cannot be less than the 'Min Rental Price'.")

        #make sure available_from is not greater than available_to
        if available_from and available_to and available_from > available_to:
            self.add_error('available_to', "The 'Available To' date cannot be earlier than the 'Available From' date.")
        
        return cleaned_data