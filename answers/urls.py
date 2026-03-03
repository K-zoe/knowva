from django.urls import path
from answers.views.list import CourseQuizListView
from answers.views.answer import (
    AnswerStartView,
    AnswerResumeView,
    AnswerRetryWrongView,
    AnswerFeedbackView
)

urlpatterns = [
    path('course_quiz_list/<int:course_pk>/', CourseQuizListView.as_view(), name = 'course_quiz_list'),

    path('answer_start/<int:course_pk>/<int:quiz_pk>/', AnswerStartView.as_view(), name = 'answer_start'),
    path('answer_resume/<int:course_pk>/<int:quiz_pk>/', AnswerResumeView.as_view(), name = 'answer_resume'),
    path('answer_retry_wrong/<int:quiz>/', AnswerRetryWrongView.as_view(), name = 'answer_retry_wrong'),

    path('answer_feedback/<int:quiz>/<int:question>/', AnswerFeedbackView.as_view(), name = 'answer_feedback'),
]
