from django_components import Component, register

from dashboard.services.grade import GradeService


@register("grade")
class Grade(Component):
    template_file = "grade/grade.html"
    css_file = "grade/grade.css"

    def get_context_data(self, **kwargs):
        """Adds a timestamp to the context."""
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}

        grade_service = GradeService()
        context['grade'] = grade_service.calculate_avg_grade()
        context['exams'] = grade_service.count_enrollments_forming_avg_grade()
        return context
