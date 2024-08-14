from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Account(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email'])
        ]