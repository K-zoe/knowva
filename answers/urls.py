from django.urls import path
from answers.views.list import CourseQuizListView
from answers.views.answer import (
    AnswerAttempView,
    AnswerFeedbackView
)

urlpatterns = [
    path('course_quiz_list/<int:course_pk>/', CourseQuizListView.as_view(), name = 'course_quiz_list'),

    path('answer_attempt/<int:course_pk>/<int:quiz_pk>/', AnswerAttempView.as_view(), name = 'answer_attempt'),

    path('answer_feedback/<int:quiz>/<int:question>/', AnswerFeedbackView.as_view(), name = 'answer_feedback'),
]
