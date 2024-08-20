from django.db import models
from django.urls import reverse


# Create your models here.

class SickPatients(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='SICK')


class User(models.Model):
    class Status(models.IntegerChoices):
        HEALTHY = 0, 'Здоров'
        SICK = 1, 'Болен'

    name = models.CharField(max_length=255,
                            verbose_name='Имя пациента')
    second_name = models.CharField(max_length=255,
                                   verbose_name='Фамилия пациента')
    middle_name = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name='Отчество пациента')
    birthday = models.DateField(verbose_name='Дата Рождения')
    address = models.OneToOneField('Address', on_delete=models.PROTECT,
                                   related_name='User_address', verbose_name='Адрес пациента')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True,
                              verbose_name='Фото')
    status = models.BooleanField(choices=[(0, 'Здоров'), (1, 'Болен')], default=0, verbose_name='Статус')

    objects = models.Manager()
    sick_patients = SickPatients()

    def __str__(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    def get_absolute_url(self):
        return reverse('patient', kwargs={'patient_slug': self.slug})

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        indexes = [
            models.Index(fields=['slug'])
        ]


class Address(models.Model):
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=100, verbose_name='Номер и корпус дома')
    flat_number = models.IntegerField(verbose_name='Номер квартиры')

    class Meta:
        verbose_name = 'Адрес пациента'
        verbose_name_plural = 'Адреса пациентов'

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.house_number} {self.flat_number}'
