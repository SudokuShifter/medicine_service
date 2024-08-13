from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class DoctorHome(TemplateView):
    template_name = 'doctor/index.html'

    extra_context = {
        'title': 'Главная страница',
        'menu': [
            {'title': 'Рабочее расписание', 'url_name': 'schedule'},
            {'title': 'Записи пациентов', 'url_name': 'records'},
            {'title': 'Личный кабинет', 'url_name': 'appointments'},
            {'title': 'Войти', 'url_name': 'login'},
            {'title': 'Регистрация', 'url_name': 'register'},
        ]
    }