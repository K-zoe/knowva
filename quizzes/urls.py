from django.urls import path
from quizzes.views.create import (
    CourseCreateView,
    QuizCreateView,
)

urlpatterns = [
    path('cource_create/', CourseCreateView.as_view(), name = 'course_create'),
    path('quiz_create/<int:course_id>/', QuizCreateView.as_view(), name = 'quiz_create'),
]
