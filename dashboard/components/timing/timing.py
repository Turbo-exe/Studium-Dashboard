from django_components import Component, register
from ... import services

@register("timing")
class TimingComponent(Component):
    template_file = "timing/timing.html"
    css_file = "timing/timing.css"

    def get_context_data(self, **kwargs):
        """Adds a timestamp to the context."""
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        timing_service = services.Timing()

        cnt_actually_finished = timing_service.count_actually_finished_enrollments()
        cnt_acknowledged = timing_service.count_acknowledged_enrollments()
        context["finishedExamsActual"] = cnt_actually_finished + cnt_acknowledged
        context["finishedExamsPlan"] = timing_service.count_planned_finished_enrollments()
        context["activeEnrollments"] = timing_service.count_active_enrollments()
        context["futureEnrollments"] = timing_service.count_future_enrollments()
        context["finishedEnrollments"] = cnt_actually_finished
        context["acknowledgedEnrollments"] = cnt_acknowledged
        context["timeModel"] = timing_service.get_time_model_friendly_name()
        return context
