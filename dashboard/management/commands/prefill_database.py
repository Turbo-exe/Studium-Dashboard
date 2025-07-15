from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.management.commands._courses import sample_courses
from dashboard.models import Course, Degree, Semester, Exam, Student, Enrollment


class Command(BaseCommand):
    help = 'Generates sample objects and saves them to the database'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                degree = self._add_degree()
                self._add_semesters(degree=degree)
                student = self._add_student(degree=degree)
                self._add_quicklinks(student=student)
                self._add_courses_and_exams(student=student)
                self.stdout.write(self.style.SUCCESS('Database successfully prefilled'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise

    def _add_degree(self) -> Degree:
        degree = Degree(degree_type="BSC", description="Bachelor of Science (BSc) for Applied Artificial Intelligence")
        degree.save()
        return degree

    def _add_semesters(self, degree: Degree):
        year = 2024
        for i in range(1, 6):
            Semester(degree=degree, name=f"Winter {year}/{year + 1}", year=year, start_date=f"{year}-10-01",
                     end_date=f"{year + 1}-03-31").save()
            Semester(degree=degree, name=f"Sommer {year + 1}", year=year + 1, start_date=f"{year + 1}-04-01",
                     end_date=f"{year + 1}-09-30").save()
            year += 1

    def _add_student(self, degree: Degree):
        student = Student(
            name="Felix Asenbauer", first_name="Felix", last_name="Asenbauer",
            semester_id=2,
            email="asenbauerfelix@outlook.com", time_model=48, started_on="2024-10-01", degree=degree
        )
        student.save()
        return student

    def _add_quicklinks(self, student: Student):
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

    def _add_courses_and_exams(self, student: Student):
        for course_data in sample_courses:
            semester = Semester.objects.get(identifier=course_data["semester"])
            course = Course.objects.create(
                code=course_data["short_code"],
                name=course_data["course_name"],
                semester=semester,
                description="",
                ects=course_data["ects"]
            )
            course.save()
            exam = Exam(course=course, exam_type=course_data["exam_type"])
            exam.save()
            status = course_data["status"]
            Enrollment(status=status, student=student, course=course,
                       score=course_data.get("score", None)).save()
