from django_components import Component, register


@register("box")
class Box(Component):
    template_file = "box/box.html"
    css_file = "box/box.css"

    def get_context_data(self, class_name="", box_id="", **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        context['class_name'] = class_name
        context['box_id'] = box_id
        return context
