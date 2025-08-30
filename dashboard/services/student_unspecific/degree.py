from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from dashboard.models import Degree


class DegreeService:
    """Service class for managing Degree objects."""

    def get_all_degrees(self) -> QuerySet:
        return Degree.objects.all()

    def get_degree_by_id(self, degree_id: int) -> Degree:
        return get_object_or_404(Degree, identifier=degree_id)

    def add_degree(self, name: str, degree_type: str, description: str = "") -> Degree:
        degree = Degree(
            name=name,
            degree_type=degree_type,
            description=description
        )
        degree.save()
        return degree

    def update_degree(self, degree_id: int, name: str = None, degree_type: str = None,
                      description: str = None) -> Degree:
        degree = self.get_degree_by_id(degree_id)

        if name is not None:
            degree.name = name
        if degree_type is not None:
            degree.degree_type = degree_type
        if description is not None:
            degree.description = description

        degree.save()
        return degree

    def delete_degree(self, degree_id: int) -> None:
        degree = self.get_degree_by_id(degree_id)
        degree.delete()
