from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from dashboard.services.student_specific._base import BaseService
from dashboard.models import Status, Course
from dashboard.models.enrollment import Enrollment


class EnrollmentsService(BaseService):

    def get_students_enrollments(self) -> QuerySet:
        enrollments = Enrollment.objects.filter(
            student=self._student
        ).select_related('course')
        return enrollments

    def add_enrollment(self, course: Course) -> Enrollment:
        enrollment = Enrollment(
            student=self._student,
            course=course,
            status=Status.AVAILABLE
        )
        enrollment.save()
        return enrollment

    def get_enrollment_by_id(self, enrollment_id: int) -> Enrollment:
        return get_object_or_404(Enrollment, id=enrollment_id, student=self._student)

    def update_enrollment(self, enrollment_id: int, status: Status, score: int or None) -> None:
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=self._student)
        enrollment.status = status
        enrollment.score = score
        enrollment.save()

    def delete_enrollment(self, enrollment_id: int) -> None:
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=self._student)
        enrollment.delete()
