from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.degree import DegreeService
from dashboard.services.student_unspecific.semester import SemesterService


class Command(BaseCommand):
    help = 'Updates an existing semester'

    def add_arguments(self, parser):
        parser.add_argument('semester_id', type=int, help='ID of the semester to update')
        parser.add_argument('--name', type=str, help='New name of the semester')
        parser.add_argument('--degree_id', type=int, help='New ID of the degree this semester belongs to')
        parser.add_argument('--year', type=int, help='New academic year of the semester')
        parser.add_argument('--start_date', type=str, help='New start date of the semester (YYYY-MM-DD)')
        parser.add_argument('--end_date', type=str, help='New end date of the semester (YYYY-MM-DD)')

    def handle(self, *args, **options):
        semester_id = options['semester_id']
        name = options.get('name')
        degree_id = options.get('degree_id')
        year = options.get('year')
        start_date_str = options.get('start_date')
        end_date_str = options.get('end_date')

        if not any([name, degree_id, year, start_date_str, end_date_str]):
            self.stdout.write(self.style.WARNING('No update parameters provided. Nothing to update.'))
            return

        try:
            # Parse dates if provided
            start_date = None
            end_date = None
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            with transaction.atomic():
                # Get the degree if provided
                degree = None
                if degree_id:
                    degree_service = DegreeService()
                    degree = degree_service.get_degree_by_id(degree_id)

                # Update the semester
                semester_service = SemesterService()
                semester = semester_service.update_semester(
                    semester_id=semester_id,
                    name=name,
                    degree=degree,
                    year=year,
                    start_date=start_date,
                    end_date=end_date
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully updated semester: {semester}'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Invalid date format: {str(e)}'))
            self.stdout.write(self.style.ERROR('Date format should be YYYY-MM-DD'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
