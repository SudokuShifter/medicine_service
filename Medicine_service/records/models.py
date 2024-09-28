from django.db import models

import datetime
# Create your models here.


class ScheduleDoctor(models.Model):
    """
    Класс ScheduleDoctor - класс для определения расписания врача.
    Задаёт диапазон рабочего времени в рамках определённой даты.
    Имеет связь с моделью DoctorProfile, так чтобы у одного врача могло быть много рабочих смен,
    но конкретно эти смены принадлежали определённому врачу.
    """
    doctor = models.ForeignKey(
        'user_part.DoctorProfile',
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
        'user_part.UserProfile',
        on_delete=models.CASCADE,
        verbose_name='Пациент',
        related_name='records')
    doctor = models.ForeignKey(
        'user_part.DoctorProfile',
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
