# Generated by Django 3.2.2 on 2024-09-08 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_part', '0002_auto_20240907_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='slug',
        ),
    ]
