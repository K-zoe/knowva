from django.contrib import admin
from .models import Course, Quiz, Question, Choice

@admin.register(Course, Quiz, Question, Choice)
class CourseAdmin(admin.ModelAdmin):
    pass