from django.core.management.base import BaseCommand
from FAQ.models import Category

class Command(BaseCommand):
    help = 'Команда заполняет БД данными для создания категорий вопросов'

    def handle(self, *args, **options):
        if Category.objects.count() == 0:
            category_names = ['Вопросы', 'Жалобы', 'Предложения', 'Благодарность', 'Отзыв']
            for c_name in category_names:
                Category.objects.create(name=c_name)
            self.stdout.write(self.style.SUCCESS('Успешно заполнены данные категорий.'))
        else:
            self.stdout.write(self.style.WARNING('Категории уже существуют. Изменения не внесены.'))
        self.stdout.write(self.style.SUCCESS('Работа команды завершена.'))