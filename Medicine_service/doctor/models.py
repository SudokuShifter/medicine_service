from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Doctor(models.Model):

    name = models.CharField(max_length=255,
                            verbose_name='Имя врача')
    second_name = models.CharField(max_length=255,
                                   verbose_name='Фамилия врача')
    middle_name = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name='Отчество врача')
    position = models.OneToOneField('Position', on_delete=models.PROTECT,
                                    related_name='doctor_pos', verbose_name='Должность врача')

    def __str__(self):
        return f'{self.second_name} {self.name} {self.middle_name}'

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'
        indexes = [
            models.Index(fields=['name', 'second_name'])
        ]


class Position(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             verbose_name='Должность врача')
    description = models.TextField(blank=True, null=True,
                                   default='Описание должности', verbose_name='Описание должности')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.title
