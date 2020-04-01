from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Question, Answer


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
        ]
        widgets = {
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']
        widgets = {
            'question': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add Question'},
            )
        }
        labels = {
            'question': '',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add Answer'},
            )
        }
        labels = {
            'answer': '',
        }