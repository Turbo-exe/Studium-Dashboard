from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.course import CourseService


class Command(BaseCommand):
    help = 'Deletes an existing course'

    def add_arguments(self, parser):
        parser.add_argument('course_id', type=int, help='ID of the course to delete')
        parser.add_argument('--force', action='store_true', help='Force deletion without confirmation')

    def handle(self, *args, **options):
        course_id = options['course_id']
        force = options.get('force', False)

        try:
            service = CourseService()
            course = service.get_course_by_id(course_id)

            if not force:
                confirm = input(
                    f"Are you sure you want to delete the course '{course}'? This action cannot be undone and will delete all associated exams and enrollments. [y/N]: ")
                if confirm.lower() != 'y':
                    self.stdout.write(self.style.WARNING('Deletion cancelled.'))
                    return

            with transaction.atomic():
                service.delete_course(course_id)
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted course: {course}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
