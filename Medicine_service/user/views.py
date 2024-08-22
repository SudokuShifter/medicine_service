from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import User
from .forms import UserDataForm
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
        account = Account.objects.get(slug=self.kwargs.get('slug'))
        return account.user_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.get_object().slug
        return context


class UserDataUpdate(UpdateView):
    model = User  # Подразумеваем, что модель называется UserData
    template_name = 'user/edit_data.html'
    context_object_name = 'user_data'
    slug_url_kwarg = 'slug'
    form_class = UserDataForm  # Предполагается, что у вас есть форма UserDataForm

    def get_object(self, queryset=None):
        # Получаем текущий аккаунт по slug
        account = Account.objects.get(slug=self.kwargs.get('slug'))
        # Проверяем, существует ли уже связанный объект User_data
        if hasattr(account, 'user_data') and account.user_data:
            return account.user_data
        else:
            # Если объект User_data не существует, создаем его
            return User(user=account.user)

    def form_valid(self, form):
        # Убедимся, что данные сохраняются
        form.instance.user = self.get_object().user  # Устанавливаем пользователя для User_data
        return super().form_valid(form)

    def get_success_url(self):
        user = self.get_object().user
        return reverse_lazy('profile', kwargs={'slug': user.account.slug})
