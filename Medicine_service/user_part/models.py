import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


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
        db_index=True,
        unique=True)
    address = models.OneToOneField(
        'Address',
        on_delete=models.SET_NULL,
        related_name='user_profile',
        null=True, blank=True)
    records = models.ManyToManyField(
        'DoctorProfile',
        through='records.PatientRecord',
        related_name='patients_records'
    )

    def __str__(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['created']
        permissions = [
            ('can_view_profile', 'Может смотреть свой профиль'),
            ('can_edit_profile', 'Может редактировать свой профиль'),
            ('can_edit_record', 'Может редактировать запись к врачу'),
            ('can_ask_question', 'Может задавать вопросы'),
            ('can_delete_quetstion', 'Может удалять вопросы'),
            ('can_view_doctor_list', 'Может смотреть список докторов'),
            ('can_change_rating_doctors', 'Может менять рейтинг докторов'),
            ('can_create_record', 'Может создавать записи к врачу'),
            ('can_view_records', 'Может смотреть записи'),
            ('can_update_records', 'Может менять записи'),
            ('can_delete_records', 'Может удалять записи'),
        ]

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

    Так же имеет связь с моделью PatientDoctorRelation из приложения records.
    PatientDoctorRelation-модель отвечает за лайки и дизлайки, которые можно будет поставить врачу.
    Она имеет внешний ключ к Пациенту и к Доктору, что и означает своеобразную ManyToMany связь.
    Чтобы обозначить вспомогательную таблицу конкретной моделью, я использовал параметр through
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
    birthday = models.DateField(
        verbose_name='Дата Рождения',
        default=datetime.date.today().strftime('%Y-%m-%d'))
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
        related_name='doctors',
        null=True, blank=True)
    address = models.OneToOneField(
        'Address',
        on_delete=models.SET_NULL,
        related_name='doctor_profile',
        null=True, blank=True)
    slug = models.SlugField(
        db_index=True,
        unique=True)
    patients = models.ManyToManyField(
        'UserProfile',
        through='records.PatientDoctorRelation',
        related_name='doctors'
    )

    def __str__(self):
        return f'{self.name} {self.second_name} {self.middle_name} в должности {self.position}'

    def get_name(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'
        permissions = [
            ('can_view_profile', 'Может смотреть свой профиль'),
            ('can_edit_profile', 'Может редактировать свой профиль'),
            ('can_edit_record_status', 'Может редактировать статус записи'),
            ('can_answer_to_question', 'Может отвечать на вопросы пользователя'),
            ('can_view_doctors_rating', 'Может смотреть рейтинг докторов'),
            ('can_view_records_patient', 'Может смотреть записи'),
        ]


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


