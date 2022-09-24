
"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from users.models import CustomUser


class CustomUserAdmin(CustomUser):
    """User model admin."""

    list_display = ('email', 'is_staff')
    list_filter = ('is_staff',)

admin.site.register(CustomUser)
admin.site.register(CustomUserAdmin)