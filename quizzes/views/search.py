from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from quizzes.models import (
    Course,
    Quiz,
    Question,
    Choice
)
from quizzes.forms.search import CourseSearchForm

class CourseSearchView(ListView):
    template_name = 'answers/course_search.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            is_public = True,
            quiz__is_public = True
        ).distinct()

        self.form = CourseSearchForm(self.request.GET)

        queryset = self.form.filter_queryset(queryset)

        return queryset