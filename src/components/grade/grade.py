# components/grade/grade.py
import time

from django_components import Component, register


@register("grade")
class Grade(Component):
    template_file = "grade/grade.html"
    css_file = "grade/grade.css"


    def get_context_data(self, **kwargs):
        """Adds a timestamp to the context."""
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        context['grade'] = "2,1"
        context['exams'] = 6
        return context

    def get_css_dependencies(self, **kwargs):
        """Appends a version to each CSS file, which avoids potential caching issues."""
        # Get the original CSS dependencies
        css_deps = super().get_css_dependencies(**kwargs)

        # Add version parameter to each CSS file
        timestamp = int(time.time())
        versioned_deps = []
        for dep in css_deps:
            if isinstance(dep, str):
                dep = f"{dep}?v={timestamp}"
            versioned_deps.append(dep)

        return versioned_deps
