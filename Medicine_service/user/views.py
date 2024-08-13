from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class UserHome(TemplateView):
    template_name = 'user/index.html'

    extra_context = {
        'title': 'Главная страница',
        'menu': [
            {'title': 'Расписание врачей', 'url_name': 'schedule'},
            {'title': 'Записи', 'url_name': 'records'},
            {'title': 'Назначения', 'url_name': 'appointments'},
            {'title': 'Советы', 'url_name': 'recs'},
            {'title': 'Личный кабинет', 'url_name': 'recs'},
            {'title': 'Войти', 'url_name': 'login'},
            {'title': 'Регистрация', 'url_name': 'register'},
        ]
    }