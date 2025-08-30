from datetime import datetime

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from dashboard.models import Student, Degree, Semester
from dashboard.models.choices import TimeModel


class StudentService:
    """
    Service class for managing Student objects.
    Note: This service does not inherit from BaseService because it is user independent.
    """

    def get_all_students(self) -> QuerySet:
        return Student.objects.all()

    def get_students_by_degree(self, degree_id: int) -> QuerySet:
        return Student.objects.filter(identifier=degree_id)

    def get_students_by_semester(self, semester_id: int) -> QuerySet:
        return Student.objects.filter(identifier=semester_id)

    def get_student_by_id(self, student_id: int) -> Student:
        return get_object_or_404(Student, identifier=student_id)

    def add_student(self, name: str, first_name: str, last_name: str, email: str,
                    degree: Degree, semester: Semester, time_model: TimeModel = TimeModel.FULL_TIME,
                    started_on: datetime = None) -> Student:
        if started_on is None:
            started_on = datetime.now()

        student = Student(
            name=name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            degree=degree,
            semester=semester,
            time_model=time_model,
            started_on=started_on
        )
        student.save()
        return student

    def update_student(self, student_id: int, name: str = None, first_name: str = None,
                       last_name: str = None, email: str = None, degree: Degree = None,
                       semester: Semester = None, time_model: TimeModel = None) -> Student:
        student = self.get_student_by_id(student_id)

        if name is not None:
            student.name = name
        if first_name is not None:
            student.first_name = first_name
        if last_name is not None:
            student.last_name = last_name
        if email is not None:
            student.email = email
        if degree is not None:
            student.degree = degree
        if semester is not None:
            student.semester = semester
        if time_model is not None:
            student.time_model = time_model

        student.save()
        return student

    def delete_student(self, student_id: int) -> None:
        student = self.get_student_by_id(student_id)
        student.delete()
