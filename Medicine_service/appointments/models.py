from datetime import timedelta

from django.db import models

# Create your models here.


class ScheduleDoctor(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT, related_name='doc', verbose_name='График Врача')
    start_at = models.DateTimeField(verbose_name='Время начала смены')
    end_at = models.DateTimeField(verbose_name='Время окончания смены')

    class Meta:
        verbose_name = 'График Врача'
        verbose_name_plural = 'График Врачей'
        ordering = ['-start_at']
        indexes = [
            models.Index(fields=['doctor'])
        ]

    def __str__(self):
        return f'{self.doctor} {self.start_at} {self.end_at}'


class PatientRecord(models.Model):
    FIXED_APPOINTMENT_DURATION = timedelta(minutes=20)

    patient = models.ForeignKey('user.Patient', on_delete=models.CASCADE, verbose_name='Пациент')
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.PROTECT, verbose_name='Врач')
    schedule = models.ForeignKey('ScheduleDoctor', on_delete=models.PROTECT, verbose_name='График Врача')
    appointment_time = models.DateTimeField(verbose_name='Время записи')

    class Meta:
        verbose_name = 'Запись пациента'
        verbose_name_plural = 'Записи пациентов'
        ordering = ['-appointment_time']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['doctor', 'shedule']),
        ]

    def __str__(self):
        return f'{self.patient} записан к {self.doctor} на {self.appointment_time}'

    def get_end_time(self):
        return self.appointment_time + self.FIXED_APPOINTMENT_DURATION


class Appointments(models.Model):
    patient = models.ForeignKey('user.Patient', on_delete=models.CASCADE, verbose_name='Пациент')
    patient_record = models.ForeignKey('PatientRecord', on_delete=models.CASCADE, verbose_name='Запись')
    comment = models.TextField()

    class Meta:
        verbose_name = 'История болезни и рекомендации'
