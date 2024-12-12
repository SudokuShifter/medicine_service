import os
from datetime import datetime

from dotenv import load_dotenv

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .models import UserProfile, Address, DoctorProfile, Position
from .logic import calculate_age

load_dotenv()


class CustomCreateUserForm(UserCreationForm):
    """
    Класс CustomCreateUserForm наследуется от UserCreationForm (заготовленный класс джанги
    для создания BaseUser.
    В классе определено доп. поле code для регистрации доктора.
    Так же внутри формы реализованы валидаторы полей и переопределен метод save
    для корректного сохранения объекта моделию.
    И определили 2 метода для определения принадлежности аккаунта к той или иной модели
    - это create_profile и some_profile_create
    """
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

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Введённые пароли не совпадают')
        if len(password1) <= 8:
            raise forms.ValidationError('Введенный пароль должен быть больше 8 символов')
        check_digit = list(filter(lambda x: x.isdigit(), set(password1)))
        if not len(check_digit):
            raise forms.ValidationError('Пароль должен содержать не только строчные символы, но и цифры')
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        code = self.cleaned_data.get('code')
        # Проверка инвайт-кода
        invite_code = os.getenv('INVITE_CODE')
        if code and invite_code and code == invite_code:
            user.is_staff = True  # Если код правильный, делаем пользователя врачом (staff)
        if commit:
            user.save()  # Сохранить пользователя перед созданием профиля
        # Создать профиль и slug после сохранения пользователя
        self.create_profile(user)
        return user

    def create_profile(self, user: User):
        """
        Создаем профиль и slug для врача или обычного пользователя
        """
        if user.is_staff:
            # Создание профиля врача, если его нет
            self.some_profile_create(DoctorProfile, user)
        else:
            # Создание обычного профиля пользователя
            self.some_profile_create(UserProfile, user)

    def some_profile_create(self, some_profile: DoctorProfile | UserProfile, user: User):
        profile, created = some_profile.objects.get_or_create(user=user)
        profile.slug = f'{slugify(self.cleaned_data.get("username"))}-{user.id}'
        profile.save()


class CustomUpdateUserForm(forms.ModelForm):
    """
    CustomUpdateUserForm - форма для создания иои обновления информации в профиле юзера.
    """
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

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        birthday_to_check = calculate_age(birthday)
        if birthday_to_check < 18:
            raise forms.ValidationError('К сожалению, пользоваться ресурсом можно только от 18ти лет')
        return birthday


class CustomUpdateDoctorForm(forms.ModelForm):
    """
    CustomUpdateDoctorForm - форма для создания или обновления информации в профили врача
    """
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=True, label='Должность')

    class Meta:
        model = DoctorProfile
        fields = [
            'name', 'second_name',
            'middle_name', 'birthday',
            'photo'
        ]
        labels = {
            'name': 'Имя',
            'second_name': 'Фамилия',
            'middle_name': 'Отчество',
            'photo': 'Фотография',
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        position = self.cleaned_data.get('position')
        user.position = position
        user.save()
        return user


class CustomUpdateUserAddressForm(forms.ModelForm):
    """
    CustomUpdateUserAddressForm - форма для создания или обновления адреса врача или юзера
    (в зависимости от клиента)
    """
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