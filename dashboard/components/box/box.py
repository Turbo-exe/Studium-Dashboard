from django_components import Component, register


@register("box")
class Box(Component):
    template_file = "box/box.html"
    css_file = "box/box.css"

    def get_context_data(self, box_class="", box_id="", **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        context['box_class'] = box_class
        context['box_id'] = box_id
        return context
