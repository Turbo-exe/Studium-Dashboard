from datetime import date

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from dashboard.models import Semester, Degree


class SemesterService:
    """Service class for managing Semester objects."""

    def get_all_semesters(self) -> QuerySet:
        return Semester.objects.all()

    def get_semesters_by_degree(self, degree_id: int) -> QuerySet:
        return Semester.objects.filter(identifier=degree_id)

    def get_semester_by_id(self, semester_id: int) -> Semester:
        return get_object_or_404(Semester, identifier=semester_id)

    def add_semester(self, name: str, degree: Degree, year: int, start_date: date, end_date: date) -> Semester:
        semester = Semester(
            name=name,
            degree=degree,
            year=year,
            start_date=start_date,
            end_date=end_date
        )
        semester.save()
        return semester

    def update_semester(self, semester_id: int, name: str = None, degree: Degree = None,
                        year: int = None, start_date: date = None, end_date: date = None) -> Semester:
        semester = self.get_semester_by_id(semester_id)

        if name is not None:
            semester.name = name
        if degree is not None:
            semester.degree = degree
        if year is not None:
            semester.year = year
        if start_date is not None:
            semester.start_date = start_date
        if end_date is not None:
            semester.end_date = end_date

        semester.save()
        return semester

    def delete_semester(self, semester_id: int) -> None:
        semester = self.get_semester_by_id(semester_id)
        semester.delete()
