# Generated by Django 3.2.2 on 2024-11-11 14:11

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_auto_20241111_1551'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='patientrecord',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='patientrecord',
            name='status',
            field=models.CharField(choices=[('IN', 'В работе'), ('CL', 'Закрыта')], default=('IN', 'В работе'), max_length=20),
        ),
    ]