from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .users import CustomUser
from .info_users import CtLocation
from wpo_logic.models import CtSport


class Profile(models.Model):
    """Profile model.

    Proxy model that extends the base data with other
    information.
    """
    profile_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    profile_aliases = models.CharField(_('Alias'), max_length=60, null=True)
    profile_picture = models.ImageField(_('Foto de perfil'), upload_to='users/pictures/', null=True, blank=True)
    profile_phone = models.CharField(_('Número movil'), max_length=15, null=True, blank=True)
    profile_is_valid_phone = models.BooleanField(_('Móvil validado'), default=False)
    location = models.ForeignKey(CtLocation, on_delete=models.CASCADE, null=True, blank=True)
    profile_date_of_birth = models.DateField(_('Fecha de nacimiento'), null=True, blank=True)
    profile_antiphishing = models.CharField(_('Antiphishing'), max_length=8, null=True)
    profile_facebook = models.CharField(_('Instagram'), max_length=50, null=True, blank=True)
    profile_instagram = models.CharField(_('LinkedIn'), max_length=50, null=True, blank=True)
    profile_twitter = models.CharField(_('Twitter'), max_length=50, null=True, blank=True)
    profile_gender = models.CharField(_('Gender'), max_length=30, null=True, blank=True)
    profile_is_public = models.BooleanField(default=True)
    sport = models.ForeignKey(CtSport, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.profile_aliases

    def save(self, *args, **kwargs):
        if not self.profile_aliases:
            self.profile_aliases = slugify(self.profile_aliases)
        super(Profile, self).save(*args, **kwargs)
