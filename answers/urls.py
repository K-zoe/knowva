from django.urls import path
from answers.views.answer import (
    AnswerAttemptView,
    AnswerFeedbackView
)

urlpatterns = [
    path('answer_attempt/<uuid:course_uuid>/<uuid:quiz_uuid>/', AnswerAttemptView.as_view(), name = 'answer_attempt'),
    path('answer_feedback/<uuid:course_uuid>/<uuid:quiz_uuid>/<int:index>', AnswerFeedbackView.as_view(), name = 'answer_feedback'),
]
