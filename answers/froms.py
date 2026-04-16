from django import forms
from quizzes.models import Choice

class AnswerFrom(forms.Form):
    choice = forms.MultipleChoiceField(
        choices = [],
        widget = forms.CheckboxSelectMultiple,
    )