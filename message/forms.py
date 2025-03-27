from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Type a message...', 'rows': 4, 'cols': 50}),
        }
