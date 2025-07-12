from django.db.models import QuerySet

from .auth import AuthService
from ..models.enrollment import Enrollment


class CoursesService:
    def __init__(self):
        self.auth_service = AuthService()
        self._student = self.auth_service.get_authenticated_student()

    def get_all_enrollments(self) -> QuerySet:
        enrollments = Enrollment.objects.filter(
            student=self._student
        ).select_related('course')
        return enrollments
