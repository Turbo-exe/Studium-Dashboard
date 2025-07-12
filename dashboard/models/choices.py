"""
This module contains all the TextChoices classes used throughout the models
to provide consistent enumeration types for various fields.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class DegreeType(models.TextChoices):
    BACHELOR = 'BSC', _('Bachelor')
    MASTER = 'MSC', _('Master')
    PHD = 'PHD', _('Promotion')


class ExamType(models.TextChoices):
    ADVANCED_WORKBOOK = 'WB', _('Advanced workbook')
    PORTFOLIO = 'PO', _('Portfolio')
    PROJECT_REPORT = 'RE', _('Project report')
    WRITTEN_EXAM = 'WE', _('Written exam')
    PRESENTATION = 'PR', _('Presentation')
    CASE_STUDY = 'CS', _('Case study')
    THESIS = "TH", _("Theses")


class Status(models.TextChoices):
    AVAILABLE = 'AVL', _('Available')
    ENROLLED = 'ENR', _('Enrolled')
    COMPLETED = 'CMP', _('Completed')
    ACKNOWLEDGED = 'ACK', _('Acknowledged')
    FAILED = 'FAL', _('Failed')

    def get_status_display(self):
        return self.label


class TimeModel(models.IntegerChoices):
    FULL_TIME = 36, _('Full-time')
    PART_TIME_1 = 48, _('Part-time 1')
    PART_TIME_2 = 72, _('Part-time 2')
