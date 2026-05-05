from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from quizzes.models import (
    Course,
    Quiz,
    Question,
    Choice
)
from answers.models import QuizSession
from django.db.models import Prefetch

class CourseDetailView(LoginRequiredMixin, DetailView):
    #NOTE: ユーザーの回答状況も表示するため、
    template_name = 'quizzes/course_detail.html'
    model = Course
    context_object_name = 'course'
    slug_field = 'uuid'
    slug_url_kwarg = 'course_uuid'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            is_public = True,
            quiz__is_public = True
        ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        user = self.request.user
        quizzes = course.quiz.filter(
            is_public = True
            ).prefetch_related(
                Prefetch(
                    'sessions',
                    queryset = QuizSession.objects.filter(user = user),
                    to_attr = 'user_sessions'
                    )
                )

        context.update({
            'course':course,
            'quizzes':quizzes,
        })

        return context