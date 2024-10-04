from django.db import models
from django.utils import timezone

import datetime
# Create your models here.


class PatientRecord(models.Model):
    """
    Класс PatientRecord - класс, отвечающий за запись пациента к врачу на определённую дату и время.
    Имеет связь с моделью UserProfile, так чтобы у одного пациента могло быть много записей,
    но при этом конкретная запись принадлежала лишь 1-му пациенту.
    Имеет связь с моделью DoctorProfile, так чтобы у одного врача могло быть много записей,
    но конкретная запись принадлежала лишь 1-му врачу.
    """

    patient = models.ForeignKey(
        'user_part.UserProfile',
        on_delete=models.CASCADE,
        verbose_name='Пациент',
        related_name='doctor_records')
    doctor = models.ForeignKey(
        'user_part.DoctorProfile',
        on_delete=models.PROTECT,
        verbose_name='Врач',
        related_name='patient_records')
    create_at = models.DateTimeField(
        auto_now_add=True
    )
    description_patient = models.TextField(
        verbose_name='заметки пациента'
    )
    description = models.TextField(
        verbose_name='Заметки врача')

    class Meta:
        verbose_name = 'Запись пациента'
        verbose_name_plural = 'Записи пациентов'
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['doctor']),
        ]

    def __str__(self):
        return f'{self.patient} записан к {self.doctor}'


class PatientStory(models.Model):
    patient = models.OneToOneField(
        'user_part.UserProfile',
        on_delete=models.CASCADE,
        verbose_name='История болезни пациента',
        related_name='story')
    doctor = models.ForeignKey(
        'user_part.DoctorProfile',
        on_delete=models.PROTECT,
        verbose_name='История болезни пациента',
        related_name='story_patient'
    )
    description = models.TextField(
        blank=True, null=True)


class PatientDoctorRelation(models.Model):
    patient = models.ForeignKey(
        'user_part.UserProfile',
        on_delete=models.CASCADE,
        related_name='rating'
    )
    doctor = models.ForeignKey(
        'user_part.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='rating'
    )
    like = models.BooleanField(
        default=False
    )
    dislike = models.BooleanField(
        default=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient',  'doctor'], name='patient_doctor_unique')
        ]