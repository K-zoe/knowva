from django.urls import path
from .views.create import (
    CourseCreateView,
    QuizCreateView,
    QuestionCreateView,
)
from .views.edit import(
    CourseEditTopView,
    quiz_delete_view,
)

urlpatterns = [
    path('cource_create/', CourseCreateView.as_view(), name = 'course_create'),
    path('quiz_create/<int:course_id>/', QuizCreateView.as_view(), name = 'quiz_create'),
    path('question_create/<int:quiz_id>/', QuestionCreateView.as_view(), name = 'question_create'),
    
    path('cource_edit_top/<int:pk>', CourseEditTopView.as_view(), name = 'course_edit_top'),
    
    path('quiz_delete/<int:course_pk>/<int:quiz_pk>/', quiz_delete_view, name = 'quiz_delete'),
]
