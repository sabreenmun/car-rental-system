from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Reviewer and reviewed_user will be set automatically

    # You may add any custom validation or other features here if needed
