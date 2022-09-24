from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from .info_users import CtState


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(_('email'), unique=True, max_length=255)
    user_name = models.CharField(_('nombre'), max_length=100, null=False)
    user_last_name = models.CharField(_('apellido'), max_length=100, null=False)
    state = models.ForeignKey(CtState, on_delete=models.CASCADE, default=1)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        indexes = [models.Index(fields=['email', ])]

    def __str__(self):
        return self.email
