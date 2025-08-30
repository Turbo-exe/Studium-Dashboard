from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.student import StudentService


class Command(BaseCommand):
    help = 'Deletes an existing student'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=int, help='ID of the student to delete')
        parser.add_argument('--force', action='store_true', help='Force deletion without confirmation')

    def handle(self, *args, **options):
        student_id = options['student_id']
        force = options.get('force', False)

        try:
            service = StudentService()
            student = service.get_student_by_id(student_id)

            if not force:
                confirm = input(
                    f"Are you sure you want to delete the student '{student}'? This action cannot be undone and will delete all associated enrollments. [y/N]: ")
                if confirm.lower() != 'y':
                    self.stdout.write(self.style.WARNING('Deletion cancelled.'))
                    return

            with transaction.atomic():
                service.delete_student(student_id)
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted student: {student}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
