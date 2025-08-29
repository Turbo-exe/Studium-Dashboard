import django_tables2 as tables
from django_components import Component, register

from dashboard.services.enrollments import EnrollmentsService
from .filters import EnrollmentsFilter
from .forms import EditEnrollmentForm, AddEnrollmentForm
from .table import EnrollmentsTable


@register("enrollments")
class EnrollmentsComponent(Component):
    template_file = "enrollments/enrollments.html"
    css_file = "enrollments/enrollments.css"
    js_file = "enrollments/enrollments.js"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}

        # Get enrollments data
        enrollments_service = EnrollmentsService()
        enrollments = enrollments_service.get_students_enrollments()

        # Create request object with enrollments data for the FilteredTableView
        request = kwargs.get('request', self.request)
        request.enrollments = enrollments

        # Create table and filter
        filter_data = request.POST if request.method == 'POST' else request.GET
        filter_instance = EnrollmentsFilter(data=filter_data, queryset=enrollments)
        table_instance = EnrollmentsTable(filter_instance.qs)
        tables.RequestConfig(request=request, paginate={"per_page": 10}).configure(table_instance)

        # Get available courses for add modal
        from dashboard.models import Course
        available_courses = Course.objects.all()

        # Create forms
        add_form = AddEnrollmentForm()
        edit_form = EditEnrollmentForm()

        # Add to context
        context['filter'] = filter_instance
        context['table'] = table_instance
        context['available_courses'] = available_courses
        context['add_form'] = add_form
        context['edit_form'] = edit_form

        return context
