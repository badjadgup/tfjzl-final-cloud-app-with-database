from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Choice, Course, Enrollment, Submission


def index(request):
    return render(request, 'onlinecourse/course_list.html', {'courses': Course.objects.order_by('name')})


def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related('lesson_set', 'question_set__choice_set'), pk=course_id)
    enrolled = request.user.is_authenticated and Enrollment.objects.filter(user=request.user, course=course).exists()
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course, 'enrolled': enrolled})


@login_required
@require_POST
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('onlinecourse:course_details', course_id=course.pk)


@login_required
@require_POST
@transaction.atomic
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, course=course, user=request.user)
    questions = list(course.question_set.prefetch_related('choice_set'))
    if not questions:
        return HttpResponseBadRequest('This course has no exam questions yet.')
    selected_ids = set()
    score = 0
    for question in questions:
        try:
            selected = {int(value) for value in request.POST.getlist(f'question_{question.pk}')}
        except (TypeError, ValueError):
            return HttpResponseBadRequest('Invalid choice identifier.')
        valid_ids = {choice.pk for choice in question.choice_set.all()}
        if not selected <= valid_ids:
            return HttpResponseBadRequest('A selected choice does not belong to this question.')
        correct_ids = {choice.pk for choice in question.choice_set.all() if choice.is_correct}
        if correct_ids and selected == correct_ids:
            score += question.grade
        selected_ids.update(selected)
    submission = Submission.objects.create(
        enrollment=enrollment, score=score, max_score=sum(q.grade for q in questions),
    )
    submission.choices.set(Choice.objects.filter(pk__in=selected_ids))
    return redirect('onlinecourse:show_exam_result', course_id=course.pk, submission_id=submission.pk)


@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related('enrollment__course'),
        pk=submission_id, enrollment__course_id=course_id, enrollment__user=request.user,
    )
    selected_ids = set(submission.choices.values_list('pk', flat=True))
    course = submission.enrollment.course
    results = []
    for question in course.question_set.prefetch_related('choice_set'):
        choices = list(question.choice_set.all())
        correct_ids = {choice.pk for choice in choices if choice.is_correct}
        results.append({
            'question': question,
            'correct': bool(correct_ids) and correct_ids == (selected_ids & {c.pk for c in choices}),
            'choices': [{'text': c.choice_text, 'selected': c.pk in selected_ids, 'correct': c.is_correct} for c in choices],
        })
    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course, 'submission': submission, 'results': results,
    })
