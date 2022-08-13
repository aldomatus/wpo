from django.db import models


class CtSport(models.Model):
    sport_id = models.SmallAutoField(primary_key=True)
    sport_name = models.CharField(unique=True, max_length=100)
    sport_slug = models.SlugField(unique=True, max_length=255)
    sport_status = models.BooleanField(default=1)

    class Meta:
        verbose_name = 'CtSport'
        verbose_name_plural = 'CtSports'
        ordering = ['sport_id']

        indexes = [models.Index(fields=['sport_name', ]),
                   models.Index(fields=['sport_slug', ])]
