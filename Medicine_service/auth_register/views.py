from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Account
from .forms import RegisterForm, LoginForm
# Create your views here.


class RegisterView(CreateView):
    model = Account
    form_class = RegisterForm
    template_name = 'auth_register/register_auth.html'
    success_url = reverse_lazy('home')


class AuthView(LoginView):
    form_class = LoginForm
    redirect_field_name = 'home'
    template_name = 'auth_register/register_auth.html'
