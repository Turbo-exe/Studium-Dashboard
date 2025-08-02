from django.db.models import QuerySet

from ._base import BaseService
from ..models.enrollment import Enrollment


class EnrollmentsService(BaseService):

    def get_students_enrollments(self) -> QuerySet:
        """Get all enrollments of a student."""
        enrollments = Enrollment.objects.filter(
            student=self._student
        ).select_related('course')
        return enrollments
