from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from source.settings import INVITE_CODE
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
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 999 99 99'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'invite_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Инвайт код (если вы врач)'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        spec_symbols = ['_', '/', '.', ',', '-', '=', '`']
        if len(password) > 6 and set(spec_symbols).intersection(set(password)):
            return password
        raise ValidationError(f'Пароль должен иметь больше 6 символов и содержать спец-символы: {" ".join(spec_symbols)}')

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        if invite_code:
            if invite_code == INVITE_CODE:
                return invite_code
            else:
                raise ValidationError('Вы ввели неверный инвайт-код')

    def save(self, commit=True):
        account = super().save(commit=False)
        invite_code = self.cleaned_data.get('invite_code')
        if invite_code == INVITE_CODE:
            doctor_group, flag = Group.objects.get_or_create(name='Doctor')
            account.is_doctor = True
            account.groups.add(doctor_group)
        if commit:
            account.set_password(self.cleaned_data['password'])
            account.save()
        return account

