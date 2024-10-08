# Generated by Django 3.2.2 on 2024-10-04 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_auto_20241004_1533'),
        ('user_part', '0015_doctorprofile_patients'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='records',
            field=models.ManyToManyField(related_name='patients_records', through='records.PatientRecord', to='user_part.DoctorProfile'),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='birthday',
            field=models.DateField(default='2024-10-04', verbose_name='Дата Рождения'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(default='2024-10-04', verbose_name='Дата Рождения'),
        ),
    ]
