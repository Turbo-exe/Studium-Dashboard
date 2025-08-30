from dashboard.services.student_specific.auth import AuthService


class BaseService:
    def __init__(self):
        self._auth_service = AuthService()
        self._student = self._auth_service.get_authenticated_student()
