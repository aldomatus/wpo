from django.db import models
from django.utils.translation import gettext_lazy as _

class CtCountry(models.Model):
    country_id = models.SmallAutoField(primary_key=True)
    country_name = models.CharField(_('nombre del pais'), max_length=100, unique=True)
    country_slug = models.CharField(null=False, unique=True, max_length=120)
    country_abbreviation = models.CharField(null=False, unique=True, max_length=2)
    country_political_division = models.CharField(null=False, max_length=60)
    country_status = models.BooleanField(null=False, default=False)

    class Meta:
        indexes = [models.Index(fields=['country_name', ]),
                   models.Index(fields=['country_slug', ]),]

    def __str__(self):
        return self.paiPais


class CtState(models.Model):
    state_id = models.SmallAutoField(primary_key=True)
    state_name = models.CharField(_('nombre de estado'), max_length=100, unique=True)
    state_slug = models.SlugField(null=False, unique=True, max_length=120)
    state_status = models.BooleanField(null=False, default=False)
    country = models.ForeignKey(CtCountry, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=['state_name', ]),
                   models.Index(fields=['country_id', 'state_name', ]),
                   models.Index(fields=['state_slug', ])]
        constraints = [
            models.UniqueConstraint(fields=['country_id', 'state_name'], name='unique_country_state'),
            models.UniqueConstraint(fields=['country_id', 'state_slug'], name='unique_country_state_slug')
        ]

    def __str__(self):
        return self.state_name


class CtLocation(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    location_name = models.CharField(_('nombre de la localidad'), max_length=160)
    state = models.ForeignKey(CtState, on_delete=models.CASCADE)
    location_slug = models.SlugField(null=False, max_length=180)
    location_status = models.BooleanField(null=False, default=True)

    class Meta:
        indexes = [models.Index(fields=['location_name', ]),
                   models.Index(fields=['state_id', 'location_name', ]),
                   models.Index(fields=['location_slug', ])]
        constraints = [
            models.UniqueConstraint(fields=['state_id', 'location_name'], name='unique_state_location'),
            models.UniqueConstraint(fields=['state_id', 'location_slug'], name='unique_state_location_slug')
        ]

    def __str__(self):
        return self.location_name


class CtDomainWhitelist(models.Model):
    domain_wl_id = models.SmallAutoField(primary_key=True)
    domain_wl_dominio = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'domain whitelist'
        verbose_name_plural = 'domain whitelist'
        ordering = ['domain_wl_id']
        indexes = [models.Index(fields=['domain_wl_dominio', ])]


    def __str__(self):
        return self.domain_wl_dominio