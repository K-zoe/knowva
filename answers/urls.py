from django.urls import path
from answers.views.answer import (
    AnswerAttempView,
    AnswerFeedbackView
)

urlpatterns = [
    path('answer_attempt/<uuid:course_uuid>/<uuid:quiz_uuid>/', AnswerAttempView.as_view(), name = 'answer_attempt'),
    path('answer_feedback/<uuid:course_uuid>/<uuid:quiz_uuid>/<int:index>', AnswerFeedbackView.as_view(), name = 'answer_feedback'),
]
