from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import User
from .forms import UserData
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


class UserLk(CreateView):
    model = User
    form_class = UserData
    template_name = 'user/lk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_title'] = 'Сохранить'
        return context


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


# class UserDataUpdate(UpdateView):
#     fields = ['name', 'second_name', 'middle_name', 'birthday', 'address', 'photo']
#     model = User
#     template_name = 'user/edit_data.html'
#     context_object_name = 'user'
#     slug_url_kwarg = 'slug'