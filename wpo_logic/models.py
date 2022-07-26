from django.db import models
from django.utils import timezone


class CtSport(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=255)
    status = models.BooleanField(default=1)

    class Meta:
        verbose_name = 'CtSport'
        verbose_name_plural = 'CtSports'
        ordering = ['id']

        indexes = [models.Index(fields=['name', ]),
                   models.Index(fields=['slug', ])]


class SportsLocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(null=False, max_length=200)
    street = models.CharField(null=False, max_length=200)
    ext_number = models.CharField(null=False, max_length=200)
    int_number = models.CharField(null=False, max_length=200)
    suburb = models.CharField(null=False, max_length=200)
    city = models.CharField(null=False, max_length=200)
    municipio = models.CharField(null=False, max_length=200, default=None)
    country = models.CharField(null=False, max_length=200)
    zip_code = models.CharField(null=False, max_length=200)
    web = models.URLField(default=None, null=True)
    facebook = models.URLField(default=None, null=True)
    instagram = models.URLField(default=None, null=True)
    map_image_url = models.URLField(default=None, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    status = models.BooleanField(default=1)
    is_active = models.BooleanField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class CodigosPostales(models.Model):
    codigo_postal_id = models.IntegerField(primary_key=True)
    codigo_postal = models.CharField(unique=False, max_length=30)
    asentamiento = models.CharField(unique=False, max_length=100)
    tipo_asentamiento = models.CharField(unique=False, max_length=100)
    municipio = models.CharField(unique=False, max_length=200)
    estado = models.CharField(unique=False, max_length=100)
    ciudad = models.CharField(unique=False, max_length=100)

