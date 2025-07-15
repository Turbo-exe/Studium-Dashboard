from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedEntity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['updated_at']
        verbose_name = _("time stamped entity")
        verbose_name_plural = _("time stamped entities")
