from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard.services.student_unspecific.exam import ExamService


class Command(BaseCommand):
    help = 'Deletes an existing exam'

    def add_arguments(self, parser):
        parser.add_argument('exam_id', type=int, help='ID of the exam to delete')
        parser.add_argument('--force', action='store_true', help='Force deletion without confirmation')

    def handle(self, *args, **options):
        exam_id = options['exam_id']
        force = options.get('force', False)

        try:
            service = ExamService()
            exam = service.get_exam_by_id(exam_id)

            if not force:
                confirm = input(
                    f"Are you sure you want to delete the exam '{exam}'? This action cannot be undone. [y/N]: ")
                if confirm.lower() != 'y':
                    self.stdout.write(self.style.WARNING('Deletion cancelled.'))
                    return

            with transaction.atomic():
                service.delete_exam(exam_id)
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted exam: {exam}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            self.stdout.write(self.style.ERROR('All database changes have been rolled back'))
            raise
