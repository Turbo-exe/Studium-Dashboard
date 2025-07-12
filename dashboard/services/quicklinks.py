from dashboard.services.auth import AuthService


class QuicklinksService:
    def __init__(self):
        self.auth_service = AuthService()
        self._student = self.auth_service.get_authenticated_student()

    def get_quicklinks_for_student(self):
        """Returns a list of quicklinks that are available for the student."""
        return self._student.quicklinks.all()
