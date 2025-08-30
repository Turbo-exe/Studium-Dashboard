from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.models.choices import TimeModel
from dashboard.services.student_unspecific.degree import DegreeService
from dashboard.services.student_unspecific.semester import SemesterService
from dashboard.services.student_unspecific.student import StudentService


class Command(BaseCommand):
    help = 'Creates a new student'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the student')
        parser.add_argument('first_name', type=str, help='First name of the student')
        parser.add_argument('last_name', type=str, help='Last name of the student')
        parser.add_argument('email', type=str, help='Email of the student')
        parser.add_argument('degree_id', type=int, help='ID of the degree this student is enrolled in')
        parser.add_argument('semester_id', type=int, help='ID of the semester this student is currently in')
        parser.add_argument('--time_model', type=int, choices=[TimeModel.FULL_TIME, TimeModel.PART_TIME],
                            default=TimeModel.FULL_TIME, help='Time model of the student (48=full-time, 24=part-time)')
        parser.add_argument('--started_on', type=str, help='Date when the student started (YYYY-MM-DD)')

    def handle(self, *args, **options):
        name = options['name']
        first_name = options['first_name']
        last_name = options['last_name']
        email = options['email']
        degree_id = options['degree_id']
        semester_id = options['semester_id']
        time_model = options['time_model']
        started_on_str = options.get('started_on')

        try:
            # Parse date if provided
            started_on = None
            if started_on_str:
                started_on = datetime.strptime(started_on_str, '%Y-%m-%d')

            with transaction.atomic():
                # Get the degree and semester
                degree_service = DegreeService()
                degree = degree_service.get_degree_by_id(degree_id)

                semester_service = SemesterService()
                semester = semester_service.get_semester_by_id(semester_id)

                # Create the student
                student_service = StudentService()
                student = student_service.add_student(
                    name=name,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    degree=degree,
                    semester=semester,
                    time_model=time_model,
                    started_on=started_on
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created student: {student}'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Invalid date format: {str(e)}'))
            self.stdout.write(self.style.ERROR('Date format should be YYYY-MM-DD'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
