from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import magic

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

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            return photo

        # MIME-тип проверки
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(photo.read(1024))
        valid_mime_types = ['image/jpeg', 'image/png']

        if mime_type not in valid_mime_types:
            raise ValidationError('Неверный формат фотографии. Разрешение файла должно быть JPG или PNG.')

        # Проверка размера файла (например, 5 МБ)
        if photo.size > 5 * 1024 * 1024:
            raise ValidationError('Размер файла слишком большой (максимум 5 МБ).')

        # Проверка размера изображения
        width, height = get_image_dimensions(photo)
        if width > 5000 or height > 5000:
            raise ValidationError('Разрешение изображения слишком большое (максимум 5000x5000 пикселей).')

        return photo

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