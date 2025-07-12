from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import Status
from .course import Course
from .exam import Exam
from .student import Student


class Enrollment(models.Model):
    """
    Represents the relationship between a student, course and exam.

    This model stores information about a student's enrollment in a course,
    including the associated exam, score and status.
    """
    student = models.ForeignKey(
        to=Student,
        related_name='student_module_exam_mappings',
        on_delete=models.CASCADE,
        help_text=_("The student enrolled in the course")
    )
    course = models.ForeignKey(
        to=Course,
        related_name='student_module_exam_mappings',
        on_delete=models.CASCADE,
        help_text=_("The course the student is enrolled in")
    )
    exam = models.ForeignKey(
        to=Exam,
        related_name='student_module_exam_mappings',
        on_delete=models.CASCADE,
        help_text=_("The exam associated with this enrollment")
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True,
        blank=True,
        help_text=_("The student's score for this exam (0.0 to 100.0)")
    )
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        db_index=True,
        help_text=_("The current status of this enrollment")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student', 'course']
        verbose_name = _("enrollment")
        verbose_name_plural = _("enrollment")
        unique_together = ['student', 'course', 'exam']

    def clean(self):
        """
        Validate that the score is within the valid range if provided.
        """
        if self.score is not None and (self.score < 0.0 or self.score > 100.0):
            raise ValidationError(_('Score must be between 0.0 and 100.0.'))

    def __str__(self):
        return f"{self.student.name} - {self.course.name} ({self.get_status_display()})"
