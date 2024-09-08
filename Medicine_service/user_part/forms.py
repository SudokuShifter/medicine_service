from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class CustomCreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Иван Иванов'}),
            'email': forms.TextInput(attrs={'placeholder': 'name@example.com'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        }
        labels = {
            'username': 'Имя',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля'

        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя пользователя уже существует")
        return username


class CustomUpdateUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'name', 'second_name',
            'middle_name', 'birthday',
            'photo']
        labels = {
            'name': 'Имя',
            'second_name': 'Фамилия',
            'middle_name': 'Отчество',
            'photo': 'Фотография'
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }