from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.models.choices import TimeModel
from dashboard.services.student_unspecific.degree import DegreeService
from dashboard.services.student_unspecific.semester import SemesterService
from dashboard.services.student_unspecific.student import StudentService


class Command(BaseCommand):
    help = 'Updates an existing student'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=int, help='ID of the student to update')
        parser.add_argument('--name', type=str, help='New name of the student')
        parser.add_argument('--first_name', type=str, help='New first name of the student')
        parser.add_argument('--last_name', type=str, help='New last name of the student')
        parser.add_argument('--email', type=str, help='New email of the student')
        parser.add_argument('--degree_id', type=int, help='New ID of the degree this student is enrolled in')
        parser.add_argument('--semester_id', type=int, help='New ID of the semester this student is currently in')
        parser.add_argument('--time_model', type=int, choices=[TimeModel.FULL_TIME, TimeModel.PART_TIME],
                            help='New time model of the student (48=full-time, 24=part-time)')

    def handle(self, *args, **options):
        student_id = options['student_id']
        name = options.get('name')
        first_name = options.get('first_name')
        last_name = options.get('last_name')
        email = options.get('email')
        degree_id = options.get('degree_id')
        semester_id = options.get('semester_id')
        time_model = options.get('time_model')

        if not any([name, first_name, last_name, email, degree_id, semester_id, time_model]):
            self.stdout.write(self.style.WARNING('No update parameters provided. Nothing to update.'))
            return

        try:
            with transaction.atomic():
                # Get the degree and semester if provided
                degree = None
                if degree_id:
                    degree_service = DegreeService()
                    degree = degree_service.get_degree_by_id(degree_id)

                semester = None
                if semester_id:
                    semester_service = SemesterService()
                    semester = semester_service.get_semester_by_id(semester_id)

                # Update the student
                student_service = StudentService()
                student = student_service.update_student(
                    student_id=student_id,
                    name=name,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    degree=degree,
                    semester=semester,
                    time_model=time_model
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully updated student: {student}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
