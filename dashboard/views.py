import json
import logging
import time

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from dashboard.components.enrollments.forms import AddEnrollmentForm, EditEnrollmentForm
from dashboard.services.student_specific.enrollments import EnrollmentsService
from dashboard.services.student_specific.quicklinks import QuicklinksService


def index(request):
    return render(
        request=request,
        template_name='index.html',
        context={
            'version': int(time.time())  # Unix timestamp; This is used that no cached frontend styled are displayed
        })


def get_enrollment(request, enrollment_id):
    enrollments_service = EnrollmentsService()
    try:
        enrollment = enrollments_service.get_enrollment_by_id(enrollment_id=enrollment_id)
        return JsonResponse(
            status=200,
            data=model_to_dict(enrollment)
        )
    except Exception as e:
        error_message = f"Failed to load enrollment {enrollment_id}."
        logging.error(msg=error_message, exc_info=e)
        return JsonResponse(status=500, data={"message": error_message})


@require_POST
def add_enrollment(request):
    """Handle the add enrollment form submission."""
    try:
        enrollments_service = EnrollmentsService()
        form = AddEnrollmentForm(request.POST)
        if not form.is_valid():
            # If the form is invalid return a 400 response
            return JsonResponse(status=400, data={"errors": form.errors})
        # Get the cleaned data and create the enrollment
        course = form.cleaned_data.get("course")
        new_enrollment = enrollments_service.add_enrollment(course=course)
        # Return a 201 response with the new enrollment
        return JsonResponse(
            status=201,
            data=model_to_dict(new_enrollment)
        )
    except Exception as e:
        error_message = f"Failed to create the new enrollment."
        logging.error(msg=error_message, exc_info=e)
        return JsonResponse(status=500, data={"message": error_message})


@require_POST
def edit_enrollment(request, enrollment_id):
    """Handle the edit enrollment form submission."""
    enrollments_service = EnrollmentsService()
    try:
        # Get the form data
        form = EditEnrollmentForm(request.POST)

        if not form.is_valid():
            # If the form is invalid return a 400 response
            return JsonResponse(
                status=400,
                data={"errors": json.dumps(form.errors.get_json_data())}
            )
        # Get the cleaned data
        status = form.cleaned_data.get("status")
        score = form.cleaned_data.get("score")

        # Update the enrollment
        enrollments_service.update_enrollment(
            enrollment_id=enrollment_id,
            status=status,
            score=score
        )
        return JsonResponse(status=204, data={})

    except Exception as e:
        error_msg = f"An unexpected error occurred while updating the enrollment {enrollment_id}."
        logging.error(error_msg, exc_info=e)
        return JsonResponse(status=500, data={"message": error_msg})


@require_POST
def delete_enrollment(request, enrollment_id):
    """Handle the delete enrollment form submission."""
    enrollments_service = EnrollmentsService()
    try:
        enrollments_service.delete_enrollment(enrollment_id=enrollment_id)  # Delete the enrollment
        return JsonResponse(status=204, data={})  # Send a no-content response
    except Exception as e:
        error_msg = f"An unexpected error occurred while deleting the enrollment {enrollment_id}."
        logging.error(msg=error_msg, exc_info=e)
        return JsonResponse(status=500, data={'message': error_msg})


def get_quicklink(request, quicklink_id):
    """Get a specific quicklink by ID."""
    quicklinks_service = QuicklinksService()
    try:
        quicklink = quicklinks_service.get_quicklink_by_id(quicklink_id=quicklink_id)
        return JsonResponse(
            status=200,
            data=model_to_dict(quicklink)
        )
    except Exception as e:
        error_message = f"Failed to load quicklink {quicklink_id}."
        logging.error(msg=error_message, exc_info=e)
        return JsonResponse(status=500, data={"message": error_message})


@require_POST
def add_quicklink(request):
    """Handle the add quicklink form submission."""
    try:
        quicklinks_service = QuicklinksService()
        text = request.POST.get('text')
        url = request.POST.get('url')
        materialIconRef = request.POST.get('materialIconRef')

        if not text or not url or not materialIconRef:
            return JsonResponse(status=400, data={"errors": {"form": ["All fields are required."]}})

        new_quicklink = quicklinks_service.add_quicklink(
            text=text,
            url=url,
            materialIconRef=materialIconRef
        )

        return JsonResponse(
            status=201,
            data=model_to_dict(new_quicklink)
        )
    except Exception as e:
        error_message = f"Failed to create the new quicklink."
        logging.error(msg=error_message, exc_info=e)
        return JsonResponse(status=500, data={"message": error_message})


@require_POST
def delete_quicklink(request, quicklink_id: str):
    """Handle the delete quicklink form submission."""
    quicklinks_service = QuicklinksService()
    try:
        quicklinks_service.delete_quicklink(quicklink_id=quicklink_id)
        return JsonResponse(status=204, data={})
    except Exception as e:
        error_msg = f"An unexpected error occurred while deleting the quicklink."
        logging.error(msg=error_msg, exc_info=e)
        return JsonResponse(status=500, data={'message': error_msg})
