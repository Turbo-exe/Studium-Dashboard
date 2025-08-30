from dashboard.models import Student
from dashboard.services.student_unspecific.student import StudentService


class AuthService:
    """
    This is a dummy service that returns a student object.
    It serves as a placeholder during the prototype phase.
    In a later development phase, this service could implement an OAuth2.0 authentication mechanism.
    """

    def get_authenticated_student(self):
        StudentService().get_student_by_id(1)
        return Student.objects.all()[0]
