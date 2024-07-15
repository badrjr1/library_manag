from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
