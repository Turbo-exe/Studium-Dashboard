from enum import Enum

from django_components import Component, register


class ModalSize(Enum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"


@register("modal")
class ModalComponent(Component):
    template_file = "modal/modal.html"
    css_file = "modal/modal.css"
    js_file = "modal/modal.js"

    _modal_id: str
    _modal_title: str
    _modal_size: ModalSize
    _modal_class: str

    def get_context_data(
            self,
            modal_id: str,
            modal_title: str,
            modal_size: ModalSize,
            modal_class: str,
            **kwargs
    ):
        self._modal_id = modal_id
        self._modal_title = modal_title
        self._modal_size = ModalSize(modal_size)
        self._modal_class = modal_class
        context = super().get_context_data(**kwargs)
        if not context:
            context = {}
        context['modal_id'] = self._modal_id
        context['modal_class'] = self._modal_class
        context['modal_title'] = self._modal_title
        context['modal_size'] = self._modal_size
        return context
