from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dashboard.models import Enrollment
from dashboard.services.student_specific.auth import AuthService


class AddEnrollmentForm(forms.ModelForm):
    """Form for creating new enrollments."""

    def __init__(self, *args, **kwargs):
        self.auth_service = AuthService()
        self.student = self.auth_service.get_authenticated_student()
        super().__init__(*args, **kwargs)

        if not self.student:
            raise ValueError("Student not authenticated, can't load addable courses.")

    class Meta:
        model = Enrollment
        fields = ['course']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'})
        }
        help_texts = {
            'course': _('Select the course to enroll in')
        }

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if not course:
            raise ValidationError(_('Please select the course to enroll in.'))
        if Enrollment.objects.filter(student=self.student, course=course).exists():
            raise ValidationError(_('You are already enrolled in this course.'))
        return course


class EditEnrollmentForm(forms.ModelForm):
    """Form for editing existing enrollments."""

    class Meta:
        model = Enrollment
        fields = ['status', 'score']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '0.01'}),
        }
        help_texts = {
            'status': _('Current status of the enrollment'),
            'score': _('Score for this enrollment (0-100)'),
        }
