from django import forms
from .models import Choice

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'explanation', 'is_correct']