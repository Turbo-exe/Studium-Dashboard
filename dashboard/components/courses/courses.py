import django_tables2 as tables
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_components import Component, register

from dashboard.models import Enrollment
from dashboard.services.courses import CoursesService
from .filters import CourseFilter
from .forms import EnrollmentForm
from .table import CourseTable


@register("courses")
class Courses(Component):
    template_file = "courses/courses.html"
    css_file = "courses/courses.css"
    js_file = "courses/courses.js"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}

        # Get enrollments data
        courses_service = CoursesService()
        enrollments = courses_service.get_all_enrollments()

        # Create request object with enrollments data for the FilteredTableView
        request = kwargs.get('request', self.request)
        request.enrollments = enrollments

        # Create table and filter
        filter_data = request.POST if request.method == 'POST' else request.GET
        filter_instance = CourseFilter(data=filter_data, queryset=enrollments)
        table_instance = CourseTable(filter_instance.qs)
        tables.RequestConfig(request=request, paginate={"per_page": 10}).configure(table_instance)

        # Create form for edit modal
        form = EnrollmentForm()

        # Add to context
        context['filter'] = filter_instance
        context['table'] = table_instance
        context['form'] = form

        return context

    def edit_course(self, request, course_id):
        """Handle edit course action."""
        try:
            enrollment = get_object_or_404(Enrollment, id=course_id)

            if request.method == 'POST':
                form = EnrollmentForm(request.POST, instance=enrollment)
                if form.is_valid():
                    form.save()
                    return JsonResponse({
                        "status": "success",
                        "message": "Enrollment updated successfully"
                    })
                else:
                    # Return form errors
                    return JsonResponse({
                        "status": "error",
                        "errors": form.errors.as_json()
                    }, status=400)
            else:
                # Return enrollment data for the form
                data = {
                    "id": enrollment.id,
                    "student": enrollment.student.identifier,
                    "course": enrollment.course.identifier,
                    "exam": enrollment.exam.identifier,
                    "score": enrollment.score,
                    "status": enrollment.status
                }
                return JsonResponse({
                    "status": "success",
                    "enrollment": data
                })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
