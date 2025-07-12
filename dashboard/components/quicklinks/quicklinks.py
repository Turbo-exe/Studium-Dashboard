from dataclasses import dataclass

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_components import Component, register

from dashboard import services
from dashboard.models import Quicklink
from .forms import QuicklinkForm


@dataclass
class QuicklinkData:
    text: str
    materialIconRef: str
    url: str


@register("quicklinks")
class Quicklinks(Component):
    template_file = "quicklinks/quicklinks.html"
    css_file = "quicklinks/quicklinks.css"
    js_file = "quicklinks/quicklinks.js"

    def get_context_data(self, **kwargs):
        """Adds a timestamp to the context."""
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}

        quicklink_service = services.Quicklinks()
        context['quicklinks'] = quicklink_service.get_quicklinks_for_student()
        context['form'] = QuicklinkForm()
        return context

    def add_quicklink(self, request):
        """Handle add quicklink action."""
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = QuicklinkForm(request.POST)
            if form.is_valid():
                quicklink = form.save(commit=False)
                quicklink.student = services.Auth().get_authenticated_student()
                quicklink.save()
                return JsonResponse({
                    "success": True,
                    "message": "Quicklink added successfully"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "errors": form.errors
                })
        return JsonResponse({
            "success": False,
            "errors": {"form": ["Invalid request"]}
        })

    def delete_quicklink(self, request):
        """Handle delete quicklink action."""
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            quicklink_id = request.POST.get('quicklink_id')
            if quicklink_id:
                try:
                    quicklink = get_object_or_404(Quicklink, id=quicklink_id)
                    quicklink.delete()
                    return JsonResponse({
                        "success": True,
                        "message": "Quicklink deleted successfully"
                    })
                except Exception as e:
                    return JsonResponse({
                        "success": False,
                        "errors": {"server": [str(e)]}
                    })
            else:
                return JsonResponse({
                    "success": False,
                    "errors": {"quicklink_id": ["This field is required"]}
                })
        return JsonResponse({
            "success": False,
            "errors": {"form": ["Invalid request"]}
        })
