from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import timedelta


# Create your models here.


class MedUser(User):
    username = models.CharField(
        max_length=150,
        unique=True, verbose_name='Логин',
        validators=MinLengthValidator(6))
    email = models.EmailField(
        max_length=150,
        unique=True, verbose_name='Эл.почта')
    slug = models.SlugField(
        default=slugify(username),
        unique=True, verbose_name='Slug')


class UserProfile(models.Model):
    user = models.OneToOneField(
        'MedUser', on_delete=models.CASCADE,
        related_name='account')
    name = models.CharField(
        max_length=150,
        verbose_name='Имя пациента')
    second_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пациента')
    middle_name = models.CharField(
        max_length=150,
        verbose_name='Отчество пациента',
        blank=True, null=True)
    birthday = models.DateField(
        verbose_name='Дата Рождения')
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        verbose_name='Фото',
        default=None, blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['created']


class DoctorProfile(models.Model):
    user_profile = models.OneToOneField(
        'UserProfile', on_delete=models.CASCADE,
        related_name='doctor_profile')
    position = models.ForeignKey(
        'Position', on_delete=models.PROTECT,
        verbose_name='Должность врача', related_name='doctors')

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'


class Address(models.Model):
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        blank=True, null=True)
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        blank=True, null=True)
    street = models.CharField(
        max_length=100,
        verbose_name='Улица',
        blank=True, null=True)
    house_number = models.CharField(
        max_length=100,
        verbose_name='Номер и корпус дома',
        blank=True, null=True)
    flat_number = models.IntegerField(
        verbose_name='Номер квартиры',
        blank=True, null=True)
    profile = models.OneToOneField(
        'Profile', on_delete=models.CASCADE,
        related_name='address')

    class Meta:
        verbose_name = 'Адрес пациента'
        verbose_name_plural = 'Адреса пациентов'

    def __str__(self):
        return f'{self.country}, г.{self.city}, ул.{self.street}, д.{self.house_number}, кв.{self.flat_number}'


class Position(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Должность врача')
    description = models.TextField(max_length=1000,
                                   blank=True, null=True,
                                   default='Описание должности',
                                   verbose_name='Описание должности')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.title


class ScheduleDoctor(models.Model):
    doctor = models.ForeignKey(
        'DoctorProfile', on_delete=models.PROTECT,
        related_name='schedules')
    start_at = models.DateTimeField(
        verbose_name='Время начала смены')
    end_at = models.DateTimeField(
        verbose_name='Время окончания смены')

    class Meta:
        verbose_name = 'График Врача'
        verbose_name_plural = 'График Врачей'
        ordering = ['-start_at']
        indexes = [
            models.Index(fields=['doctor'])
        ]

    def __str__(self):
        return f'Врач {self.doctor} с графиком работы: {self.start_at} - {self.end_at}'


class PatientRecord(models.Model):
    FIXED_APPOINTMENT_DURATION = timedelta(minutes=20)

    patient = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE,
        verbose_name='Пациент',
        related_name='records')
    doctor = models.ForeignKey(
        'DoctorProfile', on_delete=models.PROTECT,
        verbose_name='Врач',
        related_name='records')
    schedule = models.ForeignKey(
        'ScheduleDoctor', on_delete=models.PROTECT,
        default=None, related_name='records')
    appointment_time = models.DateTimeField(
        verbose_name='Время записи')
    description = models.TextField(
        default='Заметки врача',
        verbose_name='История болезни')

    class Meta:
        verbose_name = 'Запись пациента'
        verbose_name_plural = 'Записи пациентов'
        ordering = ['-appointment_time']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['doctor']),
        ]

    def __str__(self):
        return f'{self.patient} записан к {self.doctor} на {self.appointment_time}'

    def get_end_time(self):
        return self.appointment_time + self.FIXED_APPOINTMENT_DURATION
