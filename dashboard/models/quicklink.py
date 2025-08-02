from django.db import models
from django.utils.translation import gettext_lazy as _

from .student import Student
from .material_icons import MATERIAL_ICONS


class Quicklink(models.Model):
    """Represents an academic semester within a degree program."""
    student = models.ForeignKey(
        to=Student,
        related_name='quicklinks',
        on_delete=models.CASCADE,
        help_text=_("The degree program this semester belongs to")
    )
    text = models.CharField(
        max_length=255,
        help_text=_("The text of the quicklink")
    )
    url = models.URLField(
        help_text=_("The URL of the quicklink")
    )
    materialIconRef = models.CharField(
        db_index=True,
        choices=MATERIAL_ICONS,
        help_text=_("The academic year of this semester")
    )

    class Meta:
        ordering = ['text']
        verbose_name = _("Quicklink")
        verbose_name_plural = _("Quicklinks")


    def __str__(self):
        return f"{self.text} ({self.materialIconRef}) pointing to {self.url}"
