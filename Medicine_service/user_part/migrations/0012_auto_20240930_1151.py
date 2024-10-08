# Generated by Django 3.2.2 on 2024-09-30 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_part', '0011_auto_20240928_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='birthday',
            field=models.DateField(default='2024-09-30', verbose_name='Дата Рождения'),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(default='2024-09-30', verbose_name='Дата Рождения'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', unique=True),
        ),
    ]
