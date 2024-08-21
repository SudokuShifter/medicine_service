from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserData
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
