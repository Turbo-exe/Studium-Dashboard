from django import forms
from django.core.validators import URLValidator

from dashboard.models import Quicklink


class AddQuicklinkForm(forms.ModelForm):

    def clean_url(self):
        url = self.cleaned_data.get('url')
        validate = URLValidator(schemes=["http", "https"])
        validate(url)
        return url

    class Meta:
        model = Quicklink
        fields = ['text', 'url', 'materialIconRef']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'materialIconRef': forms.Select(attrs={'class': 'form-control'}),
        }
