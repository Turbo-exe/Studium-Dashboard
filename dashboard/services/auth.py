from dashboard import models


class AuthService:
    """
    This is a dummy service that returns a student object.
    It could later be replaced by a real oauth based service.
    """
    def get_authenticated_student(self):
        return models.Student.objects.get(identifier=1)
