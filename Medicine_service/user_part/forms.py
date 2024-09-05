from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomCreateUserForm(UserCreationForm):
    class Meta:
        fields = [
            'first_name', 'email', 'phone', 'password1', 'password2'
        ]
        labels = {
            'first_name': 'Имя и фамилия',
            'email': 'Email',
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля'

        }
