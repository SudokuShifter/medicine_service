from django.db import models

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
                                   related_name='user_address', verbose_name='Адрес пациента',
                                   default=None, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True,
                              verbose_name='Фото')
    status = models.BooleanField(choices=[(0, 'Здоров'), (1, 'Болен')], default=0, verbose_name='Статус')

    objects = models.Manager()
    sick_patients = SickPatients()

    def __str__(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Address(models.Model):
    country = models.CharField(max_length=100, verbose_name='Страна', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, null=True)
    street = models.CharField(max_length=100, verbose_name='Улица', blank=True, null=True)
    house_number = models.CharField(max_length=100, verbose_name='Номер и корпус дома', blank=True, null=True)
    flat_number = models.IntegerField(verbose_name='Номер квартиры', blank=True, null=True)

    class Meta:
        verbose_name = 'Адрес пациента'
        verbose_name_plural = 'Адреса пациентов'

    def __str__(self):
        return f'{self.country}, г.{self.city}, ул.{self.street}, д.{self.house_number}, кв.{self.flat_number}'
