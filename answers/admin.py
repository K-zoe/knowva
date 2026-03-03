from django.contrib import admin
from .models import QuizSession,Answer

@admin.register(QuizSession,Answer)
class CourseAdmin(admin.ModelAdmin):
    pass