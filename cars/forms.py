from django import forms
from .models import *

class CarForm(forms.ModelForm):
    available_dates = forms.CharField(
        widget=forms.TextInput(attrs={"class": "datepicker", "placeholder": "Select dates"}),
        required=False
    )

    class Meta:
        model = Car
        fields = ["model", "image", "year", "mileage", "availability", "pickup_location", "rental_price", "available_dates"]

    def clean_available_dates(self):
        dates = self.cleaned_data["available_dates"]
        return dates.split(",") if dates else [] 



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
        
        # **Ensure instance exists before accessing car**
        if not self.instance.pk:  # Check if instance is new
            return cleaned_data

        if not self.instance.car:  
            raise forms.ValidationError("Car is not assigned to this booking.")

        return cleaned_data


class CarSearchForm(forms.Form):
    model = forms.CharField(required=False, max_length=100, label="Car Model")
    rental_price_min = forms.DecimalField(required=False, label="Min Rental Price", max_digits=10, decimal_places=2)
    rental_price_max = forms.DecimalField(required=False, label="Max Rental Price", max_digits=10, decimal_places=2)