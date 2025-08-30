from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.course import CourseService
from dashboard.services.student_unspecific.exam import ExamService


class Command(BaseCommand):
    help = 'Creates a new exam'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the exam')
        parser.add_argument('course_id', type=int, help='ID of the course this exam is for')
        parser.add_argument('exam_type', type=str, help='Type of the exam (e.g., WE, PO, PR, CS, RE, TH)')

    def handle(self, *args, **options):
        name = options['name']
        course_id = options['course_id']
        exam_type = options['exam_type']

        try:
            with transaction.atomic():
                # Get the course
                course_service = CourseService()
                course = course_service.get_course_by_id(course_id)

                # Create the exam
                exam_service = ExamService()
                exam = exam_service.add_exam(
                    name=name,
                    course=course,
                    exam_type=exam_type
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created exam: {exam}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
