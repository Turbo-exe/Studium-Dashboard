from django.utils import timezone

from dashboard import models
from dashboard.services.student_specific._base import BaseService


class TimingService(BaseService):

    def count_planned_finished_enrollments(self) -> int:
        """
        Returns the number of enrollments that the student is supposed to have finished in their degree
        according to their time model.
        """
        amount_all_enrollments = self.count_all_enrollments()
        perc_elapsed = self._calculate_percentage_of_degree_elapsed()
        return int(amount_all_enrollments * perc_elapsed)

    def count_all_enrollments(self) -> int:
        """Returns the total number of enrollments that the student is supposed to take in their degree."""
        return models.Enrollment.objects.filter(
            student=self._student,
        ).count()

    def count_actually_finished_enrollments(self) -> int:
        """Returns the number of enrollments that the student actually finished in their degree."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.COMPLETED,
        ).count()

    def count_acknowledged_enrollments(self) -> int:
        """Returns the number of enrollments that were acknowledged by IU due to previous experiences outside the degree."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.ACKNOWLEDGED,
        ).count()

    def count_future_enrollments(self) -> int:
        """Returns the number of enrollments that the student is supposed to take in their degree."""
        cnt_available = models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.AVAILABLE,
        ).count()
        cnt_failed = models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.FAILED,
        ).count()
        return cnt_available + cnt_failed

    def count_active_enrollments(self) -> int:
        """Returns the number of enrollments that the student is currently taking in their degree."""
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
