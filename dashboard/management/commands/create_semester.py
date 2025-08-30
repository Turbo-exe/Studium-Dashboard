from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.degree import DegreeService
from dashboard.services.student_unspecific.semester import SemesterService


class Command(BaseCommand):
    help = 'Creates a new semester'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the semester')
        parser.add_argument('degree_id', type=int, help='ID of the degree this semester belongs to')
        parser.add_argument('year', type=int, help='Academic year of the semester')
        parser.add_argument('start_date', type=str, help='Start date of the semester (YYYY-MM-DD)')
        parser.add_argument('end_date', type=str, help='End date of the semester (YYYY-MM-DD)')

    def handle(self, *args, **options):
        name = options['name']
        degree_id = options['degree_id']
        year = options['year']
        start_date_str = options['start_date']
        end_date_str = options['end_date']

        try:
            # Parse dates
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            with transaction.atomic():
                # Get the degree
                degree_service = DegreeService()
                degree = degree_service.get_degree_by_id(degree_id)

                # Create the semester
                semester_service = SemesterService()
                semester = semester_service.add_semester(
                    name=name,
                    degree=degree,
                    year=year,
                    start_date=start_date,
                    end_date=end_date
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created semester: {semester}'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Invalid date format: {str(e)}'))
            self.stdout.write(self.style.ERROR('Date format should be YYYY-MM-DD'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
