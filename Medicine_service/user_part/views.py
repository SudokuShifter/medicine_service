from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import CustomCreateUserForm, CustomUpdateUserForm
from .models import UserProfile


# Create your views here.


def home(request):
    return render(request, 'user_part/home.html')


class UserLoginView(LoginView):
    template_name = 'user_part/login_form.html'

    def get_success_url(self):
        user = self.request.user
        success_url = reverse_lazy('first_create')
        return success_url


class UserCreateView(CreateView):
    model = User
    template_name = 'user_part/register_form.html'
    form_class = CustomCreateUserForm
    success_url = reverse_lazy('first_create')


class UserLk(DetailView):
    model = UserProfile
    template_name = 'user_part/lk.html'


class UserProfileCreateView(CreateView):
    model = UserProfile
    template_name = 'user_part/edit_data.html'
    form_class = CustomUpdateUserForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            # Если у пользователя нет профиля, мы не передаем instance
            kwargs['instance'] = getattr(self.request.user, 'user_profile', None)
        return kwargs

    def form_valid(self, form):
        # Сначала сохраняем профиль пользователя
        user_profile = form.save(commit=False)
        user = self.request.user
        user_profile.user = user
        user_profile.slug = user.username
        user_profile.save()
        # После успешного создания профиля, переходим по URL
        return super().form_valid(form)

    def form_invalid(self, form):
        # Добавляем вывод ошибок формы для диагностики
        print("Form errors:", form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('lk', kwargs={'slug': self.object.user.username})

