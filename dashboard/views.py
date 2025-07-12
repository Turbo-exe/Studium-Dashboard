import time

from django.shortcuts import render

from dashboard.components.courses.courses import Courses


def index(request):
    return render(
        request=request,
        template_name='index.html',
        context={
            'version': int(time.time())  # Unix timestamp
        })


def edit_course(request, course_id):
    """
    View function for editing a course enrollment.

    This function delegates to the edit_course method of the Courses component.
    """
    courses_component = Courses()
    return courses_component.edit_course(request, course_id)
