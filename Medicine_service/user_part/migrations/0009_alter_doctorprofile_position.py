# Generated by Django 3.2.2 on 2024-09-27 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_part', '0008_doctorprofile_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='doctors', to='user_part.position', verbose_name='Должность врача'),
        ),
    ]
