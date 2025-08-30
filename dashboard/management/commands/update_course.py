from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.course import CourseService
from dashboard.services.student_unspecific.semester import SemesterService


class Command(BaseCommand):
    help = 'Updates an existing course'

    def add_arguments(self, parser):
        parser.add_argument('course_id', type=int, help='ID of the course to update')
        parser.add_argument('--name', type=str, help='New name of the course')
        parser.add_argument('--code', type=str, help='New code of the course (e.g., DLBBIM01)')
        parser.add_argument('--semester_id', type=int, help='New ID of the semester this course belongs to')
        parser.add_argument('--description', type=str, help='New description of the course')
        parser.add_argument('--ects', type=int, help='New number of ECTS credits for the course')

    def handle(self, *args, **options):
        course_id = options['course_id']
        name = options.get('name')
        code = options.get('code')
        semester_id = options.get('semester_id')
        description = options.get('description')
        ects = options.get('ects')

        if not any([name, code, semester_id, description, ects]):
            self.stdout.write(self.style.WARNING('No update parameters provided. Nothing to update.'))
            return

        try:
            with transaction.atomic():
                # Get the semester if provided
                semester = None
                if semester_id:
                    semester_service = SemesterService()
                    semester = semester_service.get_semester_by_id(semester_id)

                # Update the course
                course_service = CourseService()
                course = course_service.update_course(
                    course_id=course_id,
                    name=name,
                    code=code,
                    semester=semester,
                    description=description,
                    ects=ects
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully updated course: {course}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
