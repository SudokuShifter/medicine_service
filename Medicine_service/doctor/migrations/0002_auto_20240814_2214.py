# Generated by Django 3.2.2 on 2024-08-14 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_register', '0001_initial'),
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name': 'Доктор', 'verbose_name_plural': 'Доктора'},
        ),
        migrations.RemoveIndex(
            model_name='doctor',
            name='doctor_doct_phone_n_44f811_idx',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='time_registration',
        ),
        migrations.AddField(
            model_name='doctor',
            name='account',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to='auth_register.account', verbose_name='Аккаунт врача'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='position',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='doctor_pos', to='doctor.position', verbose_name='Должность врача'),
        ),
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.TextField(blank=True, default='Описание должности', null=True, verbose_name='Описание должности'),
        ),
        migrations.AddIndex(
            model_name='doctor',
            index=models.Index(fields=['name', 'second_name'], name='doctor_doct_name_1d0abb_idx'),
        ),
        migrations.AddIndex(
            model_name='doctor',
            index=models.Index(fields=['slug'], name='doctor_doct_slug_a17421_idx'),
        ),
    ]