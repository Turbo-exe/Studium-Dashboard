from django.utils import timezone

from dashboard import models
from dashboard.services.auth import AuthService


class TimingService:
    def __init__(self):
        self.auth_service = AuthService()
        self._student = self.auth_service.get_authenticated_student()

    def count_planned_finished_courses(self) -> int:
        """Returns the number of courses that the student is supposed to have finished in their degree."""
        amount_all_courses = self._student.degree.courses.count()
        perc_elapsed = self._calculate_percentage_of_degree_elapsed()
        return int(amount_all_courses * perc_elapsed)

    def count_actually_finished_courses(self) -> int:
        """Returns the number of courses that the student actually finished in their degree."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.COMPLETED,
        ).count()

    def count_acknowledged_courses(self) -> int:
        """Returns the number of courses that were acknowledged by IU due to previous experiences outside the degree."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.ACKNOWLEDGED,
        ).count()

    def count_future_courses(self) -> int:
        """Returns the number of courses that the student is supposed to take in their degree."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.AVAILABLE,
        ).count()

    def count_active_courses(self) -> int:
        """Returns the number of courses that the student is currently taking in their degree."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.ENROLLED,
        ).count()

    def get_time_model_friendly_name(self):
        return self._student.get_time_model_display()

    def _calculate_percentage_of_degree_elapsed(self) -> float:
        """Returns the percentage of the degree that has went by (timewise) as a value between 0 and 1"""
        start_time = self._student.started_on
        now = timezone.now()
        total_months = self._student.time_model
        elapsed_months = (now - start_time).days / 30.4375
        return elapsed_months / total_months
