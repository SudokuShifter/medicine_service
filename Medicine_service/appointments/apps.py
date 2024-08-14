from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    verbose_name = 'Записи и пр. административная информация'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'
