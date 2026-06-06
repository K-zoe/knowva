from django.urls import path
from answers.views.attempt import AttemptView
from answers.views.feedback import FeedbackView
from answers.views.result import ResultView

urlpatterns = [
    path('answer_attempt/<uuid:course_uuid>/<uuid:quiz_uuid>/', AttemptView.as_view(), name = 'answer_attempt'),
    path('answer_feedback/<uuid:course_uuid>/<uuid:quiz_uuid>/<int:index>', FeedbackView.as_view(), name = 'answer_feedback'),
    path('result/<uuid:course_uuid>/<uuid:quiz_uuid>/', ResultView.as_view(), name = 'result'),
]
