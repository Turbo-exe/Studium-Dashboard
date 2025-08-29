from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .academic_entity import AcademicEntity
from .degree import Degree


def validate_year(value):
    """Validates that the year is within a reasonable range."""
    current_year = datetime.now().year
    if value < 2000 or value > current_year + 10:
        raise ValidationError(
            _('%(value)s is not a valid year. Year must be between 2000 and %(max_year)s.'),
            params={'value': value, 'max_year': current_year + 10},
        )


class Semester(AcademicEntity):
    degree = models.ForeignKey(
        to=Degree, 
        related_name='semesters', 
        on_delete=models.CASCADE,
        help_text=_("The degree program this semester belongs to")
    )
    year = models.IntegerField(
        validators=[validate_year],
        db_index=True,
        help_text=_("The academic year of this semester")
    )
    start_date = models.DateField(
        help_text=_("The start date of this semester")
    )
    end_date = models.DateField(
        help_text=_("The end date of this semester")
    )

    class Meta:
        ordering = ['-year', 'start_date']
        verbose_name = _("semester")
        verbose_name_plural = _("semesters")
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F('end_date')),
                name='start_date_before_end_date'
            )
        ]

    def clean(self):
        """
        Validate that start_date is before end_date.
        """
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError(_('Start date must be before end date.'))

    def __str__(self):
        return f"{self.name} ({self.year}): {self.start_date} to {self.end_date}"