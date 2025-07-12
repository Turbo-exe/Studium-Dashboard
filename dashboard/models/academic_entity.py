from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class AcademicEntity(models.Model):

    identifier = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        help_text=_("The name of this academic entity"),
        validators=[MinLengthValidator(2)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = _("academic entity")
        verbose_name_plural = _("academic entities")

    def __str__(self):
        return f"{self.name} (ID: {self.identifier})"
