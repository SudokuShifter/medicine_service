from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Question(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True)
    description = models.TextField()
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='questions')
    patient = models.ForeignKey(
        'user_part.UserProfile',
        on_delete=models.CASCADE,
        related_name='questions'
    )

    class Meta:
        verbose_name = 'Вопрос пациента'
        verbose_name_plural = 'Вопросы пациентов'


class Answer(models.Model):
    answer = models.TextField()
    doctor = models.ForeignKey(
        'user_part.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='answers')
    question = models.OneToOneField(
        'Question',
        on_delete=models.CASCADE,
        related_name='answer')