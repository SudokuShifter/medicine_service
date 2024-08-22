# Generated by Django 3.2.2 on 2024-08-21 15:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_register', '0010_auto_20240821_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='Логин'), max_length=255, unique=True, verbose_name='Slug'),
        ),
    ]