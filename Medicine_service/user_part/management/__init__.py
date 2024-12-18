from django.core.management.base import BaseCommand
from FAQ.models import Category

class Command(BaseCommand):
    help = 'Команда заполняет БД данными для создания вопроса'

    def handle(self, *args, **options):
        if Category.objects.count() == 0:
            category_names = ['Вопросы', 'Жалобы', 'Предложения', 'Благодарность', 'Отзыв']
            for c_name in category_names:
                Category.objects.create(name=c_name)
            self.stdout.write('Success fill data categories')
        else:
            self.stdout.write(self.style.WARNING('Категории уже существуют. Изменения не внесены.'))
        self.stdout.write('End work')