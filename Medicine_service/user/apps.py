from django.apps import AppConfig


class UserConfig(AppConfig):
    verbose_name = 'Пациенты'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
