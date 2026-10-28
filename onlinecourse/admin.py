from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']
    list_filter = ['course']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ['name', 'pub_date']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'enrollment', 'score', 'max_score', 'submitted_at']
    readonly_fields = ['enrollment', 'choices', 'score', 'max_score', 'submitted_at']

    def has_add_permission(self, request):
        return False


admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Choice)
