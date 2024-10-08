# Generated by Django 3.2.2 on 2024-09-04 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя врача')),
                ('second_name', models.CharField(max_length=150, verbose_name='Фамилия врача')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество врача')),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Доктор',
                'verbose_name_plural': 'Доктора',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Должность врача')),
                ('description', models.TextField(blank=True, default='Описание должности', max_length=1000, null=True, verbose_name='Описание должности')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя пациента')),
                ('second_name', models.CharField(max_length=150, verbose_name='Фамилия пациента')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество пациента')),
                ('birthday', models.DateField(verbose_name='Дата Рождения')),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(default='djangodbmodelsfieldscharfield', max_length=150, verbose_name='slug')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пациент',
                'verbose_name_plural': 'Пациенты',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleDoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField(verbose_name='Время начала смены')),
                ('end_at', models.DateTimeField(verbose_name='Время окончания смены')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedules', to='user_part.doctorprofile')),
            ],
            options={
                'verbose_name': 'График Врача',
                'verbose_name_plural': 'График Врачей',
                'ordering': ['-start_at'],
            },
        ),
        migrations.CreateModel(
            name='PatientRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_time', models.DateTimeField(verbose_name='Время записи')),
                ('description', models.TextField(default='Заметки врача', verbose_name='История болезни')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='user_part.doctorprofile', verbose_name='Врач')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='user_part.userprofile', verbose_name='Пациент')),
                ('schedule', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='records', to='user_part.scheduledoctor')),
            ],
            options={
                'verbose_name': 'Запись пациента',
                'verbose_name_plural': 'Записи пациентов',
                'ordering': ['-appointment_time'],
            },
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='doctors', to='user_part.position', verbose_name='Должность врача'),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name='Страна')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=100, null=True, verbose_name='Улица')),
                ('house_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер и корпус дома')),
                ('flat_number', models.IntegerField(blank=True, null=True, verbose_name='Номер квартиры')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='user_part.userprofile')),
            ],
            options={
                'verbose_name': 'Адрес пациента',
                'verbose_name_plural': 'Адреса пациентов',
            },
        ),
        migrations.AddIndex(
            model_name='scheduledoctor',
            index=models.Index(fields=['doctor'], name='user_part_s_doctor__7341b0_idx'),
        ),
        migrations.AddIndex(
            model_name='patientrecord',
            index=models.Index(fields=['patient'], name='user_part_p_patient_bdd281_idx'),
        ),
        migrations.AddIndex(
            model_name='patientrecord',
            index=models.Index(fields=['doctor'], name='user_part_p_doctor__827ff3_idx'),
        ),
    ]
