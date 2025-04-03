from django import forms
from .models import *

#create car form for car owners
class CarForm(forms.ModelForm):
    available_from = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "datepicker"}),
        required=True
    )
    available_to = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "datepicker"}),
        required=True
    )

    class Meta:
        model = Car
        fields = ["model", "image", "year", "mileage", "pickup_location", "rental_price", "available_from", "available_to"]

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_to = cleaned_data.get("available_to")

        if available_from and available_to and available_from > available_to:
            raise forms.ValidationError("Available from date cannot be after available to date.")

        return cleaned_data

#book car form for car renters
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data

#search car form for car owners/renters
class CarSearchForm(forms.Form):
    model = forms.CharField(required=False, max_length=100, label="Car Model")
    rental_price_min = forms.DecimalField(required=False, label="Min Rental Price", max_digits=10, decimal_places=2)
    rental_price_max = forms.DecimalField(required=False, label="Max Rental Price", max_digits=10, decimal_places=2)