from datetime import date
from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice


class Command(BaseCommand):
    help = 'Create a sample course and exam without modifying existing content.'

    def handle(self, *args, **options):
        course, created = Course.objects.get_or_create(
            name='SQL and Django Fundamentals',
            defaults={'description': 'Learn relational databases, SQL, and Django models.', 'pub_date': date.today()},
        )
        if not created:
            self.stdout.write('Sample course already exists; no changes made.')
            return
        Lesson.objects.create(course=course, title='Relational databases', order=1, content='Tables store rows. Primary keys identify rows. Foreign keys connect related tables.')
        Lesson.objects.create(course=course, title='Django models', order=2, content='Django models describe database entities. Migrations apply schema changes. QuerySets retrieve records.')
        questions = [
            ('Which SQL statement retrieves rows?', [('SELECT', True), ('DROP', False), ('DELETE', False)]),
            ('Which Django field represents a many-to-one relationship?', [('ForeignKey', True), ('CharField', False), ('BooleanField', False)]),
            ('Select all true statements about Django.', [('Models describe database data.', True), ('Migrations manage schema changes.', True), ('CSRF protection should be disabled for exam forms.', False)]),
        ]
        for text, choices in questions:
            question = Question.objects.create(course=course, question_text=text, grade=1)
            Choice.objects.bulk_create([Choice(question=question, choice_text=text, is_correct=correct) for text, correct in choices])
        self.stdout.write(self.style.SUCCESS('Sample course, lessons, and exam created.'))
