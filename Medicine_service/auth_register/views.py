from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Account
from .forms import RegisterForm
# Create your views here.


class RegisterView(CreateView):
    model = Account
    form_class = RegisterForm
    template_name = 'auth_register/register.html'
    success_url = reverse_lazy('home')
