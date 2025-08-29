from dataclasses import dataclass

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_components import Component, register

from dashboard import services
from dashboard.models import Quicklink
from .forms import AddQuicklinkForm


@dataclass
class QuicklinkData:
    text: str
    materialIconRef: str
    url: str


@register("quicklinks")
class QuicklinksComponent(Component):
    template_file = "quicklinks/quicklinks.html"
    css_file = "quicklinks/quicklinks.css"
    js_file = "quicklinks/quicklinks.js"

    def get_context_data(self, **kwargs):
        """Adds a timestamp to the context."""
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}

        quicklink_service = services.Quicklinks()
        context["quicklinks"] = quicklink_service.get_quicklinks_for_student()
        context["form"] = AddQuicklinkForm()
        return context
