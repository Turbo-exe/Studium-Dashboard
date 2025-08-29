from django import forms

from dashboard.models import Quicklink


class AddQuicklinkForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = Quicklink
        fields = ['text', 'url', 'materialIconRef']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'materialIconRef': forms.Select(attrs={'class': 'form-control'}),
        }
