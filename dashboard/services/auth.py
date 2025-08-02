from dashboard import models


class AuthService:
    """
    This is a dummy service that returns a student object.
    It serves as a placeholder for the actual authentication service during the prototype phase.
    In a later development phase, this service could implement an OAuth2.0 authentication mechanism.
    """
    def get_authenticated_student(self):
        return models.Student.objects.get(identifier=1)
