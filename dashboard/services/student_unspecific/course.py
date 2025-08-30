from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from dashboard.services.student_specific._base import BaseService
from dashboard.models import Course, Semester


class CourseService(BaseService):
    """Service class for managing Course objects."""

    def get_all_courses(self) -> QuerySet:
        return Course.objects.all()

    def get_courses_by_semester(self, semester_id: int) -> QuerySet:
        return Course.objects.filter(identifier=semester_id)

    def get_course_by_id(self, course_id: int) -> Course:
        return get_object_or_404(Course, identifier=course_id)

    def get_course_by_code(self, code: str) -> Course:
        return get_object_or_404(Course, code=code)

    def add_course(self, name: str, code: str, semester: Semester, description: str = "", ects: int = 5) -> Course:
        course = Course(
            name=name,
            code=code,
            semester=semester,
            description=description,
            ects=ects
        )
        course.save()
        return course

    def update_course(self, course_id: int, name: str = None, code: str = None,
                      semester: Semester = None, description: str = None, ects: int = None) -> Course:
        course = self.get_course_by_id(course_id)

        if name is not None:
            course.name = name
        if code is not None:
            course.code = code
        if semester is not None:
            course.semester = semester
        if description is not None:
            course.description = description
        if ects is not None:
            course.ects = ects

        course.save()
        return course

    def delete_course(self, course_id: int) -> None:
        course = self.get_course_by_id(course_id)
        course.delete()
