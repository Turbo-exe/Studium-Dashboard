from django_components import Component, register
from ... import services

@register("timing")
class Timing(Component):
    template_file = "timing/timing.html"
    css_file = "timing/timing.css"

    def get_context_data(self, **kwargs):
        """Adds a timestamp to the context."""
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        timing_service = services.Timing()
        context["finishedExamsActual"] = timing_service.count_actually_finished_enrollments()
        context["finishedExamsPlan"] = timing_service.count_planned_finished_enrollments()
        context["activeEnrollments"] = timing_service.count_active_enrollments()
        context["futureEnrollments"] = timing_service.count_future_enrollments()
        context["finishedEnrollments"] = timing_service.count_actually_finished_enrollments()
        context["acknowledgedEnrollments"] = timing_service.count_acknowledged_enrollments()
        context["timeModel"] = timing_service.get_time_model_friendly_name()
        return context
