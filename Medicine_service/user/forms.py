from django import forms
from django.core.exceptions import ValidationError

from .models import User, Address
import datetime


class UserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'second_name', 'middle_name', 'birthday', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # HTML5 date picker
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday > datetime.date.today():
            raise ValidationError('Введите корректную дату рождения')
        return birthday

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'house_number', 'flat_number']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер дома'}),
            'flat_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер квартиры'}),
        }