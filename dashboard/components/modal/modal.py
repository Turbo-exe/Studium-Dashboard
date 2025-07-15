from django_components import Component, register


@register("modal")
class Modal(Component):
    template_file = "modal/modal.html"
    css_file = "modal/modal.css"
    js_file = "modal/modal.js"

    def get_context_data(self, modal_id="", modal_title="", modal_size="medium", modal_class="", **kwargs):
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        context['modal_id'] = modal_id
        context['modal_class'] = modal_class
        context['modal_title'] = modal_title
        context['modal_size'] = modal_size
        return context
