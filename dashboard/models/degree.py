from django.db import models
from django.utils.translation import gettext_lazy as _

from .academic_entity import AcademicEntity
from .choices import DegreeType


class Degree(AcademicEntity):
    """
    Represents an academic degree program offered by the institution.

    This model stores information about different degree programs such as
    Bachelor's, Master's, or PhD, including their type and description.
    """
    degree_type = models.CharField(
        max_length=3, 
        choices=DegreeType.choices,
        db_index=True,
        help_text=_("The type of degree (Bachelor, Master, PhD)")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Detailed description of the degree program")
    )

    class Meta:
        ordering = ['degree_type', 'name']
        verbose_name = _("degree")
        verbose_name_plural = _("degrees")

    def __str__(self):
        return f"{self.get_degree_type_display()}: {self.name}"