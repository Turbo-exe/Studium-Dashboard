from django.shortcuts import get_object_or_404
from dashboard.services._base import BaseService
from dashboard.models.quicklink import Quicklink


class QuicklinksService(BaseService):

    def get_quicklinks_for_student(self):
        """Returns a list of quicklinks that are available for the student."""
        return self._student.quicklinks.all()

    def add_quicklink(self, text, url, materialIconRef):
        """Add a quicklink for the student."""
        quicklink = Quicklink(
            student=self._student,
            text=text,
            url=url,
            materialIconRef=materialIconRef
        )
        quicklink.save()
        return quicklink

    def get_quicklink_by_id(self, quicklink_id):
        """Get a specific quicklink by ID for the authenticated student."""
        return get_object_or_404(Quicklink, id=quicklink_id, student=self._student)

    def delete_quicklink(self, quicklink_id):
        """Delete a quicklink for the student."""
        quicklink = get_object_or_404(Quicklink, id=quicklink_id, student=self._student)
        quicklink.delete()
