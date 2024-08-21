from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm

from .models import Account
from user.forms import UserData, UserAddressForm
from .forms import RegisterForm, LoginForm
# Create your views here.


class RegisterView(CreateView):
    model = Account
    form_class = RegisterForm
    template_name = 'auth_register/register_auth.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Получаем только что зарегистрированного пользователя
        user = form.instance
        # Устанавливаем пользователя в сессии
        self.request.session['_auth_user_id'] = user.pk
        return response

    def get_success_url(self):
        # Получаем только что зарегистрированного пользователя
        user = self.object
        return reverse('profile', kwargs={'slug': user.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_title'] = 'Зарегистрироваться'
        context['user_form'] = UserData
        context['user_address'] = UserAddressForm
        return context


class AuthView(LoginView):
    form_class = LoginForm
    template_name = 'auth_register/register_auth.html'

    def get_success_url(self):
        # Получаем пользователя
        user = self.request.user
        if user.is_authenticated:
            # Используем slug для создания URL
            return reverse('profile', kwargs={'slug': user.slug})
        return super().get_success_url()

    def form_valid(self, form):
        # Переопределяем form_valid для выполнения логики при успешной авторизации
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_title'] = 'Войти'
        return context
