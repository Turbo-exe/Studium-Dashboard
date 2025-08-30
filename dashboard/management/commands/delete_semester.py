from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.semester import SemesterService


class Command(BaseCommand):
    help = 'Deletes an existing semester'

    def add_arguments(self, parser):
        parser.add_argument('semester_id', type=int, help='ID of the semester to delete')
        parser.add_argument('--force', action='store_true', help='Force deletion without confirmation')

    def handle(self, *args, **options):
        semester_id = options['semester_id']
        force = options.get('force', False)

        try:
            service = SemesterService()
            semester = service.get_semester_by_id(semester_id)

            if not force:
                confirm = input(
                    f"Are you sure you want to delete the semester '{semester}'? This action cannot be undone and will delete all associated courses and exams. [y/N]: ")
                if confirm.lower() != 'y':
                    self.stdout.write(self.style.WARNING('Deletion cancelled.'))
                    return

            with transaction.atomic():
                service.delete_semester(semester_id)
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted semester: {semester}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
