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
        widgets = {}