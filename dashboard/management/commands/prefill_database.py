from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.management.commands._courses import sample_courses
from dashboard.models import Student, Degree
from dashboard.models.choices import TimeModel
from dashboard.services.student_specific.enrollments import EnrollmentsService
from dashboard.services.student_unspecific.course import CourseService
from dashboard.services.student_unspecific.degree import DegreeService
from dashboard.services.student_unspecific.exam import ExamService
from dashboard.services.student_unspecific.semester import SemesterService
from dashboard.services.student_unspecific.student import StudentService


class Command(BaseCommand):
    help = 'Generates sample objects and saves them to the database'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                degree = self._add_degree()
                self._add_semesters(degree=degree)
                student = self._add_student(degree=degree)
                self._add_quicklinks(student=student)
                self._add_courses_and_exams()
                self.stdout.write(self.style.SUCCESS('Database successfully prefilled'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise

    def _add_degree(self) -> Degree:
        degree_service = DegreeService()
        degree = degree_service.add_degree(
            name="Applied Artificial Intelligence",
            degree_type="BSC",
            description="Bachelor of Science (BSc) for Applied Artificial Intelligence"
        )
        return degree

    def _add_semesters(self, degree: Degree) -> None:
        semester_service = SemesterService()
        year = 2024
        for i in range(1, 6):
            # Add Winter semester
            winter_start = datetime.strptime(f"{year}-10-01", "%Y-%m-%d").date()
            winter_end = datetime.strptime(f"{year + 1}-03-31", "%Y-%m-%d").date()
            semester_service.add_semester(
                name=f"Winter {year}/{year + 1}",
                degree=degree,
                year=year,
                start_date=winter_start,
                end_date=winter_end
            )

            # Add Summer semester
            summer_start = datetime.strptime(f"{year + 1}-04-01", "%Y-%m-%d").date()
            summer_end = datetime.strptime(f"{year + 1}-09-30", "%Y-%m-%d").date()
            semester_service.add_semester(
                name=f"Sommer {year + 1}",
                degree=degree,
                year=year + 1,
                start_date=summer_start,
                end_date=summer_end
            )

            year += 1

    def _add_student(self, degree: Degree) -> Student:
        student_service = StudentService()
        semester_service = SemesterService()

        # Get the second semester (Summer 2024)
        semester = semester_service.get_semester_by_id(2)

        # Parse the start date
        started_on = datetime.strptime("2024-10-01", "%Y-%m-%d").replace(
            tzinfo=datetime.now().astimezone().tzinfo
        )
        student = student_service.add_student(
            name="Felix Asenbauer",
            first_name="Felix",
            last_name="Asenbauer",
            email="asenbauerfelix@outlook.com",
            degree=degree,
            semester=semester,
            time_model=TimeModel.FULL_TIME,
            started_on=started_on
        )
        return student

    def _add_quicklinks(self, student: Student) -> None:
        student.quicklinks.create(
            text="My Campus",
            url="https://mycampus.iu.org/home",
            materialIconRef="e88a"  # home
        )
        student.quicklinks.create(
            text="FAQs",
            url="https://mycampus.iu.org/faq",
            materialIconRef="eb8b"  # question_mark
        )
        student.quicklinks.create(
            text="Kursbuchung",
            url="https://mycampus.iu.org/study-management/study-plan",
            materialIconRef="e85d"  # Assignment
        )
        student.quicklinks.create(
            text="Klausuranmeldung",
            url="https://mycampus.iu.org/study-management/examinations",
            materialIconRef="f88d"  # Edit Square
        )
        student.quicklinks.create(
            text="Profil",
            url="https://mycampus.iu.org/profile",
            materialIconRef="e855"  # Person
        )
        student.quicklinks.create(
            text="Ablaufplan (bis 31.08.25)",
            url="https://res.cloudinary.com/iugroup/image/upload/v1746189253/sap_ba_angewandte_kuenstliche_intelligenz_180_FS_BAAKI_de_fs_mhwa9j.pdf",
            materialIconRef="e878"  # Event
        )

    def _add_courses_and_exams(self) -> None:
        course_service = CourseService()
        exam_service = ExamService()
        semester_service = SemesterService()

        for course_data in sample_courses:
            # Get the semester by ID
            semester = semester_service.get_semester_by_id(course_data["semester"])

            # Create the course
            course = course_service.add_course(
                name=course_data["course_name"],
                code=course_data["short_code"],
                semester=semester,
                description="",
                ects=course_data["ects"]
            )

            # Create the exam
            exam_service.add_exam(
                name=f"Exam for {course_data['course_name']}",
                course=course,
                exam_type=course_data["exam_type"]
            )

            # Create an enrollment for the student
            enrollment_service = EnrollmentsService()
            enrollment = enrollment_service.add_enrollment(course=course)

            # Update the enrollment status and score if needed
            status = course_data.get("status", None)
            score = course_data.get("score", None)

            enrollment_service.update_enrollment(
                enrollment_id=enrollment.id,
                status=status,
                score=score
            )
