from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import User, Address
from .forms import UserDataForm, UserAddressForm
from auth_register.models import Account


# Create your views here.


class UserHome(TemplateView):
    template_name = 'user/index.html'

    extra_context = {
        'title': 'Главная страница',
        'menu': [
            {'title': 'Расписание врачей', 'url_name': 'schedule'},
            {'title': 'Записи', 'url_name': 'records'},
            {'title': 'Личный кабинет', 'url_name': 'recs'},
            {'title': 'Войти', 'url_name': 'login'},
            {'title': 'Регистрация', 'url_name': 'register'},
        ]
    }


class UserProfileView(DetailView):
    model = Account
    template_name = 'user/lk.html'
    context_object_name = 'user'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        return Account.objects.get(slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.get_object().slug
        return context


class UserUpdateView(View):
    def get(self, request, slug):
        user = User.objects.get(user_data__slug=slug)  # Приводим к единому виду
        address, created = Address.objects.get_or_create(user_address=user)  # Получаем или создаем адрес

        user_form = UserDataForm(instance=user)
        address_form = UserAddressForm(instance=address)

        return render(request, 'user/edit_data.html', {
            'user_form': user_form,
            'address_form': address_form,
            'user': user
        })

    def post(self, request, slug):
        user = User.objects.get(user_data__slug=slug)  # Приводим к единому виду
        address, created = Address.objects.get_or_create(user=user)  # Получаем или создаем адрес

        user_form = UserDataForm(request.POST, request.FILES, instance=user)
        address_form = UserAddressForm(request.POST, instance=address)

        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            return redirect('profile', slug=user.account_data.slug)  # Используем slug аккаунта

        return render(request, 'user/edit_data.html', {
            'user_form': user_form,
            'address_form': address_form,
            'user': user,
        })