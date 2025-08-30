from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.exam import ExamService


class Command(BaseCommand):
    help = 'Updates an existing exam'

    def add_arguments(self, parser):
        parser.add_argument('exam_id', type=int, help='ID of the exam to update')
        parser.add_argument('--name', type=str, help='New name of the exam')
        parser.add_argument('--exam_type', type=str, help='New type of the exam (e.g., WE, PO, PR, CS, RE, TH)')

    def handle(self, *args, **options):
        exam_id = options['exam_id']
        name = options.get('name')
        exam_type = options.get('exam_type')

        if not any([name, exam_type]):
            self.stdout.write(self.style.WARNING('No update parameters provided. Nothing to update.'))
            return

        try:
            with transaction.atomic():
                # Update the exam
                exam_service = ExamService()
                exam = exam_service.update_exam(
                    exam_id=exam_id,
                    name=name,
                    exam_type=exam_type
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully updated exam: {exam}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
