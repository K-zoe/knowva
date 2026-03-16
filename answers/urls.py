from django.urls import path
from answers.views.list import CourseQuizListView
from answers.views.answer import (
    AnswerAttempView,
    AnswerFeedbackView
)

urlpatterns = [
    path('course_quiz_list/<uuid:course_uuid>/', CourseQuizListView.as_view(), name = 'course_quiz_list'),

    path('answer_attempt/<uuid:course_uuid>/<uuid:quiz_uuid>/', AnswerAttempView.as_view(), name = 'answer_attempt'),

    path('answer_feedback/<uuid:course_uuid>/<uuid:quiz_uuid>/<int:index>', AnswerFeedbackView.as_view(), name = 'answer_feedback'),
]
