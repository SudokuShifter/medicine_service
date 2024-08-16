from django import forms
from .models import Account


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'phone_number']
        widgets = {
            'password': forms.PasswordInput(),
        }