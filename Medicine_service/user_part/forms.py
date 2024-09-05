from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomCreateUserForm(UserCreationForm):
    class Meta:
        fields = [
            'first_name', 'email', 'password1', 'password2'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Иван Иванов'}),
            'email': forms.TextInput(attrs={'placeholder': 'name@example.com'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        }
        labels = {
            'first_name': 'Имя',
            'email': 'Email',
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля'

        }
