"""
Management command to add Python-2 subject (Pandas, NumPy, Machine Learning).
Run: python manage.py add_python2_subject
Creates a semester "Python-2" and subject "Python-2" if they do not exist.
"""
from django.core.management.base import BaseCommand
from semesters.models import Semester, Subject


class Command(BaseCommand):
    help = 'Add Python-2 subject for Pandas, NumPy, Machine Learning preparation'

    def handle(self, *args, **options):
        semester, created = Semester.objects.get_or_create(
            name='Python-2',
            defaults={'description': 'Pandas, NumPy, and Machine Learning – data analysis and ML preparation'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created semester: Python-2'))
        else:
            self.stdout.write('Semester "Python-2" already exists.')

        subject, created = Subject.objects.get_or_create(
            semester=semester,
            name='Python-2',
            defaults={'code': 'PY2'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created subject: Python-2 (PY2) – add units and programming/MCQ questions from Admin.'))
        else:
            self.stdout.write('Subject "Python-2" already exists.')
        self.stdout.write('Done. Use Admin > Manage Semesters > Python-2 > Manage Subjects to add units and questions.')
