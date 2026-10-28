from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Course, Question, Choice, Enrollment, Submission


class ExamTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('learner', password='test-password-123')
        self.course = Course.objects.create(name='Test course', description='Test', pub_date=date.today())
        Enrollment.objects.create(user=self.user, course=self.course)
        self.question = Question.objects.create(course=self.course, question_text='Select both correct options', grade=3)
        self.a = Choice.objects.create(question=self.question, choice_text='A', is_correct=True)
        self.b = Choice.objects.create(question=self.question, choice_text='B', is_correct=True)
        self.c = Choice.objects.create(question=self.question, choice_text='C', is_correct=False)
        self.submit_url = reverse('onlinecourse:submit', args=[self.course.pk])
        self.client.force_login(self.user)

    def test_correct_submission_and_result_render(self):
        response = self.client.post(self.submit_url, {f'question_{self.question.pk}': [self.a.pk, self.b.pk]}, follow=True)
        self.assertContains(response, 'Congratulations!')
        submission = Submission.objects.get()
        self.assertEqual(submission.score, 3)
        self.assertEqual(submission.percentage, 100)

    def test_partial_or_extra_or_missing_choices_earn_zero(self):
        for selected in ([self.a.pk], [self.a.pk, self.b.pk, self.c.pk], []):
            self.client.post(self.submit_url, {f'question_{self.question.pk}': selected})
            self.assertEqual(Submission.objects.latest('pk').score, 0)

    def test_other_question_choices_are_rejected(self):
        other = Question.objects.create(course=self.course, question_text='Other')
        foreign = Choice.objects.create(question=other, choice_text='Foreign', is_correct=True)
        response = self.client.post(self.submit_url, {f'question_{self.question.pk}': [foreign.pk]})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Submission.objects.exists())

    def test_other_user_cannot_view_result(self):
        response = self.client.post(self.submit_url, {f'question_{self.question.pk}': [self.a.pk, self.b.pk]})
        other_user = get_user_model().objects.create_user('other')
        self.client.force_login(other_user)
        self.assertEqual(self.client.get(response.url).status_code, 404)

    def test_enrollment_and_post_required(self):
        self.assertEqual(self.client.get(self.submit_url).status_code, 405)
        Enrollment.objects.all().delete()
        self.assertEqual(self.client.post(self.submit_url).status_code, 404)

    def test_course_template_renders(self):
        self.assertContains(self.client.get(reverse('onlinecourse:course_details', args=[self.course.pk])), 'Test course')

    def test_anonymous_submission_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.post(self.submit_url).status_code, 302)
        self.assertFalse(Submission.objects.exists())

    def test_result_context_uses_all_question_weights(self):
        Question.objects.create(course=self.course, question_text='Unanswered', grade=2)
        response = self.client.post(self.submit_url, {f'question_{self.question.pk}': [self.a.pk, self.b.pk]}, follow=True)
        self.assertEqual(response.context['total_score'], 3)
        self.assertEqual(response.context['possible_score'], 5)
        self.assertEqual(response.context['grade'], 60)
        self.assertEqual(response.context['possible'], 5)
        self.assertFalse(response.context['passed'])
