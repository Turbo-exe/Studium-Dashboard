"""
Course filter implementation for the academic dashboard.

This module defines the CourseFilter class for filtering course information
using django-filters.
"""

import django_filters
from django.utils.translation import gettext_lazy as _

from dashboard import models
from dashboard.models.choices import Status


class EnrollmentsFilter(django_filters.FilterSet):
    """
    Filter for course information based on student enrollments.

    This filter provides filtering capabilities for enrollment records and their
    associated course attributes.
    """
    code = django_filters.CharFilter(
        label=_("Shortcode"),
        field_name="course__code",
        lookup_expr="icontains",
        label_suffix=""
    )
    name = django_filters.CharFilter(
        label=_("Title"),
        field_name="course__name",
        lookup_expr="icontains",
        label_suffix=""
    )
    ects = django_filters.NumberFilter(
        label=_("ECTS"),
        field_name="course__ects",
        label_suffix=""
    )
    status = django_filters.ChoiceFilter(
        label=_("Status"),
        choices=Status.choices,
        label_suffix=""
    )
    description = django_filters.CharFilter(
        label=_("Description"),
        field_name="course__description",
        lookup_expr="icontains",
        label_suffix=""
    )
    score = django_filters.NumberFilter(
        label=_("Score"),
        field_name="score",
        label_suffix="",
    )

    class Meta:
        model = models.Enrollment
        exclude = ("status", "score", 'created_at', 'updated_at', 'student', 'course', 'exam', "id", "identifier")
