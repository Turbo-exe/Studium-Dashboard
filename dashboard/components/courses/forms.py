from django import forms
from django.utils.translation import gettext_lazy as _

from dashboard.models import Enrollment, Student, Course, Exam


class EnrollmentForm(forms.ModelForm):
    """
    Form for editing enrollment records.
    """
    class Meta:
        model = Enrollment
        fields = ['score', 'status']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'score': _('Score'),
            'status': _('Status'),
        }
        help_texts = {
            'score': _('Achieved score (0 to 100)'),
            'status': _('Status of this course'),
        }

    def clean_score(self):
        """
        Validate that the score is within the valid range if provided.
        """
        score = self.cleaned_data.get('score')
        if score is not None and (score < 0.0 or score > 100.0):
            raise forms.ValidationError(_('Score must be between 0 and 100.'))
        return score
