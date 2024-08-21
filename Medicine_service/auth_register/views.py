from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Account
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
# Create your views here.


class RegisterView(CreateView):
    model = Account
    form_class = RegisterForm
    template_name = 'auth_register/register_auth.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_title'] = 'Зарегистрироваться'
        return context


class AuthView(LoginView):
    authentication_form = LoginForm
    redirect_field_name = 'home'
    template_name = 'auth_register/register_auth.html'
    success_url = reverse_lazy('lk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_title'] = 'Войти'
        return context
