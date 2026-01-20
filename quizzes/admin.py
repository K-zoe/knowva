from django.contrib import admin
from quizzes.models import Course, Quiz, Question, Choice

@admin.register(Course, Quiz, Question, Choice)
class CourseAdmin(admin.ModelAdmin):
    pass