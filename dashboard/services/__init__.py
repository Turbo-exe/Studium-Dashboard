"""
This package contains all services used throughout the application.
"""

# Note: We split services into student-specific and student-unspecific services because the student-specific services
# get a reference to the currently logged-in student. The student-unspecific services do not.
from dashboard.services.student_specific.timing import TimingService as Timing
from dashboard.services.student_specific.auth import AuthService as Auth
from dashboard.services.student_specific.quicklinks import QuicklinksService as Quicklinks
from dashboard.services.student_specific.enrollments import EnrollmentsService as Courses
from dashboard.services.student_unspecific.student import StudentService as Student
from dashboard.services.student_unspecific.course import CourseService as Course
from dashboard.services.student_unspecific.exam import ExamService as Exam
from dashboard.services.student_unspecific.semester import SemesterService as Semester
from dashboard.services.student_unspecific.degree import DegreeService as Degree
