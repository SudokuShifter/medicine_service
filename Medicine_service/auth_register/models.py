from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import Group, Permission, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    username = models.CharField(unique=True, max_length=20, validators=[MinLengthValidator(6)], verbose_name='Логин')
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email'])
        ]
