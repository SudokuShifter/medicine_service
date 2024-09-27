import os

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, Address, DoctorProfile
from source.settings import INVITE_CODE


class CustomCreateUserForm(UserCreationForm):
    code = forms.CharField(
        max_length=10, min_length=3, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Инвайт-код (если вы врач)'}))

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'code'
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
            'password2': 'Подтверждение пароля',
            'code': 'Введите код'
        }

    def clean_username(self):
        """
        Проверка уникальности юзернейма
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Имя пользователя уже существует')
        return username

    def clean_email(self):
        """
        Проверка уникальности Мейла
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный e-mail уже используется другим пользователем')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        code = self.cleaned_data.get('code')
        # Если код верный, устанавливаем is_staff = True
        if code and code == INVITE_CODE:
            user.is_staff = True

        user.save()
        return user


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


class CustomUpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            'name', 'second_name',
            'middle_name', 'birthday',
            'photo', 'position'
        ]
        labels = {
            'name': 'Имя',
            'second_name': 'Фамилия',
            'middle_name': 'Отчество',
            'photo': 'Фотография',
            'position': 'Должность'
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }


class CustomUpdateUserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'country', 'city',
            'street', 'house_number',
            'flat_number']
        labels = {
            'country': 'Страна',
            'city': 'Город',
            'street': 'Улица',
            'house_number': 'Номер дома (корпус при наличии)',
            'flat_number': 'Номер квартиры'
        }