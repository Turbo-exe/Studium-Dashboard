from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.course import CourseService
from dashboard.services.student_unspecific.semester import SemesterService


class Command(BaseCommand):
    help = 'Creates a new course'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the course')
        parser.add_argument('code', type=str, help='Code of the course (e.g., DLBBIM01)')
        parser.add_argument('semester_id', type=int, help='ID of the semester this course belongs to')
        parser.add_argument('--description', type=str, default='', help='Description of the course')
        parser.add_argument('--ects', type=int, default=5, help='Number of ECTS credits for the course')

    def handle(self, *args, **options):
        name = options['name']
        code = options['code']
        semester_id = options['semester_id']
        description = options['description']
        ects = options['ects']

        try:
            with transaction.atomic():
                # Get the semester
                semester_service = SemesterService()
                semester = semester_service.get_semester_by_id(semester_id)

                # Create the course
                course_service = CourseService()
                course = course_service.add_course(
                    name=name,
                    code=code,
                    semester=semester,
                    description=description,
                    ects=ects
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created course: {course}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
