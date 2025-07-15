from django.db import models
from django.utils.translation import gettext_lazy as _

from .academic_entity import AcademicEntity
from .choices import ExamType
from .degree import Degree
from .semester import Semester
from .course import Course


class Exam(AcademicEntity):
    """
    Represents an exam for a specific course.
    """
    course = models.OneToOneField(
        to=Course, 
        related_name='exam',
        on_delete=models.CASCADE,
        help_text=_("The course this exam is for")
    )
    exam_type = models.CharField(
        max_length=2, 
        choices=ExamType.choices,
        db_index=True,
        help_text=_("The type of examination")
    )

    class Meta:
        ordering = ['course', 'exam_type']
        verbose_name = _("exam")
        verbose_name_plural = _("exams")
        indexes = [
            models.Index(fields=['course', 'exam_type']),
        ]

    def __str__(self):
        return f"{self.get_exam_type_display()} for {self.course.name}"
