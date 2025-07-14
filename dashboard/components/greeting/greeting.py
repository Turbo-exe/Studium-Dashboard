import locale
from datetime import datetime

import pytz
from django_components import Component, register

from dashboard import services, settings


@register("greeting")
class Timing(Component):
    template_file = "greeting/greeting.html"
    css_file = "greeting/greeting.css"

    def get_context_data(self, class_name="", box_id="", **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        auth_service = services.Auth()
        context["date_string"] = self._get_date_string()
        context["student_name"] = auth_service.get_authenticated_student().first_name
        return context

    @staticmethod
    def _get_date_string():
        """Builds a date string in the format (in german) → 'Mittwoch, 26.03.2025'."""
        locale.setlocale(category=locale.LC_TIME, locale=f"{settings.LANGUAGE_CODE}.UTF-8")
        berlin_tz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.now(tz=berlin_tz)
        return now.strftime("%A, %d. %B %Y")
