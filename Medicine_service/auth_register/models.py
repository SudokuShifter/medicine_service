from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Account(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        related_name='account_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='account_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email'])
        ]