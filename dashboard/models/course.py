from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from .academic_entity import AcademicEntity
from .degree import Degree
from .semester import Semester


class Course(AcademicEntity):
    """
    Represents an academic course within a degree program and semester.

    This model stores information about courses offered in specific semesters,
    including the associated degree program, semester, description, and ECTS credits.
    """
    identifier = models.CharField(
        primary_key=True,
        unique=True,
        help_text=_("The course identifier (e.g., DLBBIM01)")
    )
    degree = models.ForeignKey(
        to=Degree, 
        related_name='courses', 
        on_delete=models.CASCADE,
        help_text=_("The degree program this course belongs to")
    )
    semester = models.ForeignKey(
        to=Semester, 
        related_name='courses', 
        on_delete=models.CASCADE,
        help_text=_("The semester in which this course is offered")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Detailed description of the course content")
    )
    ects = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        help_text=_("The number of ECTS credits for this course")
    )

    class Meta:
        ordering = ['semester', 'name']
        verbose_name = _("course")
        verbose_name_plural = _("courses")
        indexes = [
            models.Index(fields=['degree', 'semester']),
        ]

    def __str__(self):
        return f"{self.name} ({self.ects} ECTS)"
