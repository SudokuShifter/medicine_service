from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Account


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'phone_number', 'password', 'invite_code']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Эл. почта'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 999 99 99'}),
            # 'invite_code': forms.CharField(attrs={'class': 'form-control', 'placeholder': 'Инвайт-код (если вы врач)'}),
        }
