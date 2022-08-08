import os
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from .info_users import CtState
from django_cryptography.fields import encrypt


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(_('email'), unique=True, max_length=255)
    user_name = encrypt(models.CharField(_('nombre'), max_length=100, null=False), key=os.environ["DB_PASSWORD_ENCRYPT"].encode())
    user_last_name = encrypt(models.CharField(_('apellido'), max_length=100, null=False), key=os.environ["DB_PASSWORD_ENCRYPT"].encode())
    state = models.ForeignKey(CtState, on_delete=models.CASCADE, default=1)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        indexes = [models.Index(fields=['email', ])]

    def __str__(self):
        return self.email