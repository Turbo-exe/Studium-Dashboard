from dashboard import models
from dashboard.services._base import BaseService


class GradeService(BaseService):

    def calculate_avg_grade(self):
        """Calculates the average grade for the student based on their finished enrollments."""
        enrollments = self._find_finished_enrollments()
        if not enrollments.exists():
            return None

        avg_score = sum(enrollment.score for enrollment in enrollments) / self.count_enrollments_forming_avg_grade()
        return self._map_avg_score_to_grade(avg_score=avg_score)

    def count_enrollments_forming_avg_grade(self) -> int:
        """Returns the number of enrollments that are part of the average grade calculation."""
        enrollments = self._find_finished_enrollments()
        return enrollments.count()

    def count_recognized_courses(self) -> int:
        """Returns the number of courses recognized for the student based on prior experience/degrees."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.COMPLETED,
            score__isnull=True,
        ).count()

    def _find_finished_enrollments(self):
        """Returns all enrollments that have been finished by the student (excludes recognized courses)."""
        return models.Enrollment.objects.filter(
            student=self._student,
            status=models.Status.COMPLETED,
            score__isnull=False,
        )

    @staticmethod
    def _map_avg_score_to_grade(avg_score: float):
        """
        This method maps a point score to an average grade.
        This is done using this mapping: https://mycampus.iu.org/faq?activeBookingId=11263790&documentId=IU-1482109522
        """
        if avg_score >= 96:
            return 1.0
        elif avg_score >= 91:
            return 1.3
        elif avg_score >= 86:
            return 1.7
        elif avg_score >= 81:
            return 2.0
        elif avg_score >= 76:
            return 2.3
        elif avg_score >= 71:
            return 2.7
        elif avg_score >= 66:
            return 3.0
        elif avg_score >= 61:
            return 3.3
        elif avg_score >= 56:
            return 3.7
        elif avg_score >= 50:
            return 4.0
        else:
            return 5.0
