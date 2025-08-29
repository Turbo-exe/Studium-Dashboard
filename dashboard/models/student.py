from django.db import models
from django.utils.translation import gettext_lazy as _

from .academic_entity import AcademicEntity
from .choices import TimeModel
from .degree import Degree
from .semester import Semester
from .course import Course


class Student(AcademicEntity):
    first_name = models.TextField(
        verbose_name=_('first name'),
        max_length=100
    )
    last_name = models.TextField(
        verbose_name=_('last name'),
        max_length=100
    )
    email = models.EmailField(
        verbose_name=_('email'),
        max_length=100
    )
    time_model = models.IntegerField(
        verbose_name=_('time model'),
        choices=TimeModel.choices,
        default=TimeModel.FULL_TIME
    )
    started_on = models.DateTimeField(
        verbose_name=_('joined on')
    )
    degree = models.ForeignKey(
        to=Degree, 
        related_name='students', 
        on_delete=models.CASCADE,
        help_text=_("The degree program this student is enrolled in")
    )
    semester = models.ForeignKey(
        to=Semester, 
        related_name='students', 
        on_delete=models.CASCADE,
        help_text=_("The current semester of this student")
    )
    courses = models.ManyToManyField(
        to=Course, 
        related_name='students', 
        through='dashboard.Enrollment',
        help_text=_("The courses this student is enrolled in")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("student")
        verbose_name_plural = _("students")
        indexes = [
            models.Index(fields=['degree', 'semester']),
        ]

    def __str__(self):
        return f"{self.name}"


