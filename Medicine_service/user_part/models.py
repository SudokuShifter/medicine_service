from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime


# Create your models here.


class UserProfile(models.Model):
    """
    Класс UserProfile - класс с пользовательской информацией, которая будет доступна пользователю в личном кабинете.
    Класс имеет связь с моделью User, так чтобы каждый профиль был связан с конкретной учётной записью
    Из экземпляра модели MedUser можно доставать данные по UserProfile через параметр related_name - то есть 'account'.
    Например: self.user.user_profile

    Так же имеет связь с моделью Records.
    Чтобы запросить записи к врачам, нужно сделать следующее:
    self.user.user_profile.records
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='user_profile',
        blank=True, null=True)
    name = models.CharField(
        max_length=150,
        verbose_name='Имя пациента',
        blank=True, null=True)
    second_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пациента',
        blank=True, null=True)
    middle_name = models.CharField(
        max_length=150,
        verbose_name='Отчество пациента',
        blank=True, null=True)
    birthday = models.DateField(
        verbose_name='Дата Рождения',
        default=datetime.date.today().strftime('%Y-%m-%d'))
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        verbose_name='Фото',
        default=None, blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True)
    slug = models.SlugField(
        default=slugify(name))
    address = models.OneToOneField(
        'Address', on_delete=models.SET_NULL,
        related_name='profile', null=True, blank=True)

    def __str__(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['created']


class DoctorProfile(models.Model):
    """
    Класс DoctorProfile - класс профиля доктора, который будет доступен в личном кабинете.
    Класс имеет связь с моделью MedProfile, так чтобы один профиль доктора был связан с одной
    учётной записью. Из экземпляра модели User можно доставать данные по DoctorProfile
    через параметр related_name - то есть 'doctor_profile'.
    Например: self.user.doctor_profile

    Так же имеет связь через внешний ключ (Один ко многим), где у одного врача может быть лишь 1 категория,
    а в 1 категории множество врачей с моделью Position.
    Чтобы через должность посмотреть всех врачей, необходимо сделать следующее:
    self.position.doctors

    Так же имеет связь с моделью ScheduleDoctor.
    Чтобы запросить график работы, нужно сделать следующее:
    self.user.doctor_profile.schedules

    Так же имеет связь с моделью Records.
    Чтобы запросить записи пациентов, нужно сделать следующее:
    self.user.doctor_profile.records
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='doctor_profile',
        blank=True, null=True)
    name = models.CharField(
        max_length=150,
        verbose_name='Имя врача',
        blank=True, null=True)
    second_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия врача',
        blank=True, null=True)
    middle_name = models.CharField(
        max_length=150,
        verbose_name='Отчество врача',
        blank=True, null=True)
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        verbose_name='Фото',
        default=None, blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True)
    position = models.ForeignKey(
        'Position',
        on_delete=models.PROTECT,
        verbose_name='Должность врача',
        related_name='doctors')

    def __str__(self):
        return f'{self.name} {self.second_name} {self.middle_name} в должности {self.position}'

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'


class Address(models.Model):
    """
    Класс Адрес - класс для хранения данных об адресе пациента и врача,
    которые будут отображены в соотв личных кабинетах. Класс имеет связь с моделью Profile,
    так чтобы каждый профиль был связан с конкретной записью об адресе.
    Из модели UserProfile можно вытягивать адрес по параметру related_name - то есть 'address'.
    Например: self.user.user_profile.address
    """
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

    class Meta:
        verbose_name = 'Адрес пациента'
        verbose_name_plural = 'Адреса пациентов'

    def __str__(self):
        return f'{self.country}, г.{self.city}, ул.{self.street}, д.{self.house_number}, кв.{self.flat_number}'


class Position(models.Model):
    """
    Класс Position - класс для определения должности врача.
    Чтобы через должность посмотреть всех врачей, необходимо сделать следующее:
    self.position.doctors
    """
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Должность врача')
    description = models.TextField(
        max_length=1000,
        blank=True, null=True,
        default='Описание должности',
        verbose_name='Описание должности')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.title


class ScheduleDoctor(models.Model):
    """
    Класс ScheduleDoctor - класс для определения расписания врача.
    Задаёт диапазон рабочего времени в рамках определённой даты.
    Имеет связь с моделью DoctorProfile, так чтобы у одного врача могло быть много рабочих смен,
    но конкретно эти смены принадлежали определённому врачу.
    """
    doctor = models.ForeignKey(
        'DoctorProfile',
        on_delete=models.PROTECT,
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
    """
    Класс PatientRecord - класс, отвечающий за запись пациента к врачу на определённую дату и время.
    Имеет связь с моделью UserProfile, так чтобы у одного пациента могло быть много записей,
    но при этом конкретная запись принадлежала лишь 1-му пациенту.
    Имеет связь с моделью DoctorProfile, так чтобы у одного врача могло быть много записей,
    но конкретная запись принадлежала лишь 1-му врачу.

    Время посещения врача фиксировано: FIXED_APPOINTMENT_DURATION
    """

    FIXED_APPOINTMENT_DURATION = datetime.timedelta(minutes=20)

    patient = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        verbose_name='Пациент',
        related_name='records')
    doctor = models.ForeignKey(
        'DoctorProfile',
        on_delete=models.PROTECT,
        verbose_name='Врач',
        related_name='records')
    schedule = models.ForeignKey(
        'ScheduleDoctor',
        on_delete=models.PROTECT,
        default=None,
        related_name='records')
    appointment_time = models.DateTimeField(
        verbose_name='Время записи')
    description = models.TextField(
        verbose_name='Заметки врача')

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


class PatientStory(models.Model):
    patient = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name='История болезни пациента',
        related_name='story')
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        verbose_name='История болезни пациента',
        related_name='story_patient'
    )
    description = models.TextField(
        blank=True, null=True)
