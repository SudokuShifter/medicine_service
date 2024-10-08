# Generated by Django 3.2.2 on 2024-09-08 13:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_part', '0004_userprofile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя врача'),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='second_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия врача'),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(default=datetime.date(2024, 9, 8), verbose_name='Дата Рождения'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя пациента'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='second_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия пациента'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
