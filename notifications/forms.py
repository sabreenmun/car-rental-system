from django import forms
from .models import Review

#form to leave a review - renter
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  #reviewer and reviewed_user will be set automatically

    
