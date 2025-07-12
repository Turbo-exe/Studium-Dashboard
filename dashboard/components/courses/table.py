import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from dashboard import models


class ECTSColumn(tables.Column):
    @staticmethod
    def order_value(value):
        """
        Converts the ECTS value to an integer for sorting.
        W/o this the sort will yield '1, 10, 11, [...], 2, 20, ..
        """
        return int(value)


class CourseTable(tables.Table):
    """
    Table for displaying course information based on student enrollments.
    Ref. to goal 1.2 from phase 1 document.
    """
    identifier = tables.Column(
        verbose_name=_("Shortcode"),
        orderable=True,
        accessor="course.identifier"
    )
    name = tables.Column(
        verbose_name=_("Title"),
        orderable=True,
        accessor="course.name"
    )
    ects = ECTSColumn(
        verbose_name=_("ECTS"),
        orderable=True,
        accessor="course.ects"
    )
    status = tables.Column(
        verbose_name=_("Status"),
        orderable=False,
        accessor="get_status_display",
    )
    description = tables.Column(
        verbose_name=_("Description"),
        orderable=True,
        accessor="course.description"
    )
    score = tables.Column(
        verbose_name=_("Score"),
        orderable=True,
        accessor="score"
    )
    actions = tables.TemplateColumn(
        template_name="courses/_action_buttons.html",
        verbose_name=_("Actions"),
        orderable=False,
    )

    class Meta:
        model = models.Enrollment
        attrs = {
            "class": "courses-table",
        }
        sequence = (
            "identifier",
            "name",
            "ects",
            "status",
            "description",
            "score",
            "actions"
        )
        exclude = ("created_at", "updated_at", "student", "course", "exam", "id")
        empty_text = _("No courses found.")
