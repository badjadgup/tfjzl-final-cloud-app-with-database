from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True)
    social_link = models.URLField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateField()
    instructors = models.ManyToManyField(Instructor, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    content = models.TextField()

    class Meta:
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'course'], name='one_enrollment_per_course')]

    def __str__(self):
        return f'{self.user} — {self.course}'


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    grade = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        correct_ids = set(self.choice_set.filter(is_correct=True).values_list('pk', flat=True))
        return bool(correct_ids) and correct_ids == set(selected_ids)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)

    @property
    def percentage(self):
        return round(100 * self.score / self.max_score, 2) if self.max_score else 0

    @property
    def passed(self):
        return self.max_score > 0 and self.score * 100 >= self.max_score * 80

    def __str__(self):
        return f'{self.enrollment.user}: {self.score}/{self.max_score}'
