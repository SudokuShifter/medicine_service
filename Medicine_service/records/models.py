import datetime

from django.db import models
# Create your models here.


class PatientRecord(models.Model):
    """
    Класс PatientRecord - класс, отвечающий за запись пациента к врачу на определённую дату и время.
    Имеет связь с моделью UserProfile, так чтобы у одного пациента могло быть много записей,
    но при этом конкретная запись принадлежала лишь 1-му пациенту.
    Имеет связь с моделью DoctorProfile, так чтобы у одного врача могло быть много записей,
    но конкретная запись принадлежала лишь 1-му врачу.

    Имеет формат промежуточной таблицы для связи ManyToMany в модели user_part.PatientProfile
    И выглядит это следующим образом:
    records = models.ManyToManyField(
        'DoctorProfile',
        through='records.PatientRecord', ---> through ключевое слово для указания модели
        related_name='patients_records'
    )
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
    appointment_date = models.DateTimeField(
        default=datetime.date.today() + datetime.timedelta(days=1)
    )
    description_patient = models.TextField(
        blank=True, null=True,
        verbose_name='заметки пациента'
    )
    description = models.TextField(
        blank=True, null=True,
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
    """
    Класс PatientStory - класс отвечающий за сохранение в базе данных истории о болезни пациента.
    Возможность создать такую запись будет прикреплена к обработке записи со стороны врача.
    Имеет связь с пациентом в формате OneToOne, чтобы у каждого пациента была 1 конкретная мед. книжка
    И связь с доктором в формате внешнего ключа, чтобы множество врачей могли оставлять заметки.

    В планах: обдумать связь с записями !!!
    """
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
    """
    Класс PatientDoctorRelation - клас отвечающий за сохранение записей о лайках и дизлайках врачей.
    Имеет формат промежуточной таблицы для связи ManyToMany.
    Так как каждый пациент может поставить лайк множеству врачей,
    и врач может получить множество лайков от пациентов.

    При этом комбинация полей patient & doctor -- уникальна

    Указатель на эту связь находится в модели user_part.DoctorProfile и выглядит так:
    patients = models.ManyToManyField(
        'UserProfile',
        through='records.PatientDoctorRelation', ---> through ключевое слово для указания модели
        related_name='doctors'
    )
    """
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
            models.UniqueConstraint(fields=['patient', 'doctor'], name='patient_doctor_unique')
        ]
