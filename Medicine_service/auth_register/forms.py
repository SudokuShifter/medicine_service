from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Account


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Электронная почта',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'phone_number', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 999 99 99'}),
        }
