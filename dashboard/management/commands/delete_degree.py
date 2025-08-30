from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.degree import DegreeService


class Command(BaseCommand):
    help = 'Deletes an existing degree'

    def add_arguments(self, parser):
        parser.add_argument('degree_id', type=int, help='ID of the degree to delete')
        parser.add_argument('--force', action='store_true', help='Force deletion without confirmation')

    def handle(self, *args, **options):
        degree_id = options['degree_id']
        force = options.get('force', False)

        try:
            service = DegreeService()
            degree = service.get_degree_by_id(degree_id)

            if not force:
                confirm = input(
                    f"Are you sure you want to delete the degree '{degree}'? This action cannot be undone. [y/N]: ")
                if confirm.lower() != 'y':
                    self.stdout.write(self.style.WARNING('Deletion cancelled.'))
                    return

            with transaction.atomic():
                service.delete_degree(degree_id)
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted degree: {degree}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
