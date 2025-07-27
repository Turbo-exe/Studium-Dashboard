from dashboard.services._base import BaseService


class QuicklinksService(BaseService):

    def get_quicklinks_for_student(self):
        """Returns a list of quicklinks that are available for the student."""
        return self._student.quicklinks.all()
