from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from dashboard.models import Exam, Course


class ExamService:
    """Service class for managing Exam objects."""

    def get_all_exams(self) -> QuerySet:
        return Exam.objects.all()

    def get_exam_by_id(self, exam_id: int) -> Exam:
        return get_object_or_404(Exam, identifier=exam_id)

    def get_exam_by_course(self, course_id: int) -> Exam:
        return get_object_or_404(Exam, identifier=course_id)

    def add_exam(self, name: str, course: Course, exam_type: str) -> Exam:
        exam = Exam(
            name=name,
            course=course,
            exam_type=exam_type
        )
        exam.save()
        return exam

    def update_exam(self, exam_id: int, name: str = None, exam_type: str = None) -> Exam:
        exam = self.get_exam_by_id(exam_id)

        if name is not None:
            exam.name = name
        if exam_type is not None:
            exam.exam_type = exam_type

        exam.save()
        return exam

    def delete_exam(self, exam_id: int) -> None:
        exam = self.get_exam_by_id(exam_id)
        exam.delete()
