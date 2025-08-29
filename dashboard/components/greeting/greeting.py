import locale
from datetime import datetime

from django.utils.translation import get_language
from django_components import Component, register

from dashboard import services


@register("greeting")
class GreetingComponent(Component):
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
        current_language = get_language()
        try:
            if current_language == 'de':
                locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
            else:
                locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, '')

        current_date = datetime.now()
        date_string = current_date.strftime('%A, %d.%m.%Y')
        locale.setlocale(locale.LC_TIME, '')
        return date_string
