from django.shortcuts import get_object_or_404
from dashboard.services._base import BaseService
from dashboard.models.quicklink import Quicklink


class QuicklinksService(BaseService):

    def get_quicklinks_for_student(self):
        return self._student.quicklinks.all()

    def add_quicklink(self, text, url, materialIconRef):
        quicklink = Quicklink(
            student=self._student,
            text=text,
            url=url,
            materialIconRef=materialIconRef
        )
        quicklink.save()
        return quicklink

    def get_quicklink_by_id(self, quicklink_id):
        return get_object_or_404(Quicklink, id=quicklink_id, student=self._student)

    def delete_quicklink(self, quicklink_id):
        quicklink = get_object_or_404(Quicklink, id=quicklink_id, student=self._student)
        quicklink.delete()
