from django import forms

from dashboard.models import Quicklink


class QuicklinkForm(forms.ModelForm):
    class Meta:
        model = Quicklink
        fields = ['text', 'url', 'materialIconRef']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'materialIconRef': forms.Select(attrs={'class': 'form-control'}),
        }
