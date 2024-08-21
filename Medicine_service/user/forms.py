from django import forms
from django.core.exceptions import ValidationError

from .models import User
import datetime


class UserData(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'second_name', 'middle_name', 'birthday', 'address', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата рождения'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'Photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Фото'}),
        }

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday > datetime.date.today():
            raise ValidationError('Введите корректную дату рождения')
        return birthday
