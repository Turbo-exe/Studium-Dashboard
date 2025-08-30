from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.degree import DegreeService


class Command(BaseCommand):
    help = 'Updates an existing degree'

    def add_arguments(self, parser):
        parser.add_argument('degree_id', type=int, help='ID of the degree to update')
        parser.add_argument('--name', type=str, help='New name of the degree')
        parser.add_argument('--degree_type', type=str, help='New type of the degree (e.g., BSC, MSC, PHD)')
        parser.add_argument('--description', type=str, help='New description of the degree')

    def handle(self, *args, **options):
        degree_id = options['degree_id']
        name = options.get('name')
        degree_type = options.get('degree_type')
        description = options.get('description')

        if not any([name, degree_type, description]):
            self.stdout.write(self.style.WARNING('No update parameters provided. Nothing to update.'))
            return

        try:
            with transaction.atomic():
                service = DegreeService()
                degree = service.update_degree(
                    degree_id=degree_id,
                    name=name,
                    degree_type=degree_type,
                    description=description
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully updated degree: {degree}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
