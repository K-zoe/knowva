from django.urls import path
from .views.create import (
    CourseCreateView,
    QuizCreateView,
    QuestionCreateView
)

urlpatterns = [
    path('cource_create/', CourseCreateView.as_view(), name = 'course_create'),
    path('quiz_create/<int:course_id>/', QuizCreateView.as_view(), name = 'quiz_create'),
    path('question_create/<int:quiz_id>/', QuestionCreateView.as_view(), name = 'question_create'),
]
