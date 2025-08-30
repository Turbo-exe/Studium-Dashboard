from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.degree import DegreeService


class Command(BaseCommand):
    help = 'Creates a new degree'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the degree')
        parser.add_argument('degree_type', type=str, help='Type of the degree (e.g., BSC, MSC, PHD)')
        parser.add_argument('--description', type=str, default='', help='Description of the degree')

    def handle(self, *args, **options):
        name = options['name']
        degree_type = options['degree_type']
        description = options['description']

        try:
            with transaction.atomic():
                service = DegreeService()
                degree = service.add_degree(
                    name=name,
                    degree_type=degree_type,
                    description=description
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created degree: {degree}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
