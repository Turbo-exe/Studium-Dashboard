from django import forms
from django.utils.translation import gettext_lazy as _

from dashboard.models import Enrollment, choices


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

    def clean(self):
        """
        Validates if the provided score and status match each other.
        :raises ValidationError: If score is lower than 50 and status is 'passed'.
        :raises ValidationError: If score is higher than 50 and status is 'failed'.
        """
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        status = cleaned_data.get('status')
        if score is not None and status is not None:
            if status == choices.Status.COMPLETED and score < 50.0:
                raise forms.ValidationError(_('Score must be at least 50.0 when status is "passed".'))
            elif status == choices.Status.FAILED and score >= 50.0:
                raise forms.ValidationError(_('Score must be lower than 50.0 when status is "failed".'))
        return cleaned_data

    def clean_score(self) -> float:
        """
        Validates if the provided score is within the allowed range.
        :raises ValidationError: If the score is not within the allowed range.
        """
        score = self.cleaned_data.get('score')
        if score is not None and (score < 0.0 or score > 100.0):
            raise forms.ValidationError(_('Score must be between 0 and 100.'))
        return score
