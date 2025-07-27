from django_components import Component, register


@register("box")
class BoxComponent(Component):
    template_file = "box/box.html"
    css_file = "box/box.css"

    _box_class: str
    _box_id: str

    def get_context_data(self, box_class="", box_id="", **kwargs):
        self._box_class = box_class
        self._box_id = box_id
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        context['box_class'] = box_class
        context['box_id'] = box_id
        return context
