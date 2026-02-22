from django import forms
from .models import (
    Course,
    Quiz,
    Question,
    Choice
)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'tag', 'description', 'is_public']
        widgets = {
            'title':forms.TextInput(
                attrs = {'placeholder':'コース名を入力してください。'}
            ),
            'tag':forms.TextInput(
                attrs = {'placeholder':'例：#基本情報, #ITパスポート'}
            ),
            'description':forms.Textarea(
                attrs = {'placeholder':'コースの説明を入力してください。'}
            )
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']
        widgets = {
            'title':forms.TextInput(
                attrs = {'placeholder':'例：午後問題'}
            ),
            'description':forms.Textarea(
                attrs = {'placeholder':'説明を入力してください。'}
            )
        }

class QuizEditForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description','is_public']
        widgets = {
            'title':forms.TextInput(
                attrs = {'placeholder':'例：午後問題'}
            ),
            'description':forms.Textarea(
                attrs = {'placeholder':'説明を入力してください。'}
            )
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'explanation']
        widgets = {
            'title':forms.TextInput(
                attrs = {'placeholder':'タイトルを入力してください。'}
            ),
            'text':forms.Textarea(
                attrs = {'placeholder':'問題を入力してください。'}
            ),
            'explanation':forms.Textarea(
                attrs = {'placeholder':'解説を入力してください。'}
            )
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'explanation', 'is_correct']
        widgets = {
            'text':forms.Textarea(
                attrs = {'placeholder':'選択肢を入力してください。'}
            ),
            'explanation':forms.Textarea(
                attrs = {'placeholder':'解説を入力してください。'}
            )
        }