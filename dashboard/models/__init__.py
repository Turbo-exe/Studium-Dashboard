"""
Django models package for the academic dashboard.

This package contains all the models used in the academic dashboard application,
organized into separate modules for better maintainability.
"""

from .choices import DegreeType, ExamType, Status
from .academic_entity import AcademicEntity
from .degree import Degree
from .quicklink import Quicklink
from .semester import Semester, validate_year
from .course import Course
from .exam import Exam
from .student import Student
from .enrollment import Enrollment

__all__ = [
    "DegreeType",
    "ExamType",
    "Status",
    "AcademicEntity",
    "Degree",
    "Semester",
    "validate_year",
    "Course",
    "Exam",
    "Student",
    "Enrollment",
    "Quicklink",
]
