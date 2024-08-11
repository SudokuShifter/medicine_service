from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


# Create your models here.

class SickPatients(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


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
    time_registration = models.DateTimeField(auto_now_add=True,
                                             verbose_name='Время создания')
    phone_number = PhoneNumberField(null=False, blank=False, unique=True,
                                    verbose_name='Телефон пациента')
    email = models.EmailField(verbose_name='Электронная почта пациента', default=None)
    address = models.OneToOneField('Address', on_delete=models.PROTECT,
                                   related_name='User_address', verbose_name='Адрес пациента')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True,
                              verbose_name='Фото')
    status = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)))

    objects = models.Manager()
    sick_patients = SickPatients()

    def __str__(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    def get_absolute_url(self):
        return reverse('patient', kwargs={'patient_slug': self.slug})

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['-time_registration']
        indexes = [
            models.Index(fields=['phone_number', 'slug'])
        ]


class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    flat_number = models.IntegerField()

    class Meta:
        verbose_name = 'Адрес пациента'
        verbose_name_plural = 'Адреса пациентов'

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.house_number} {self.flat_number}'
