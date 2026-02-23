from django.urls import path
from .views.create import (
    CourseCreateView,
    QuizCreateView,
    QuestionCreateView,
)
from .views.edit import(
    CourseEditTopView,
    course_delete_view,
    quiz_delete_view,
    CourseEditView,
    QuizEditView,
    question_delete_view,
    QuestionEditView,
)

urlpatterns = [
    #Create
    path('cource_create/', CourseCreateView.as_view(), name = 'course_create'),
    path('quiz_create/<int:course_pk>/', QuizCreateView.as_view(), name = 'quiz_create'),
    path('question_create/<int:quiz_pk>/', QuestionCreateView.as_view(), name = 'question_create'),
    #Edit
    path('course_edit_top/<int:course_pk>/', CourseEditTopView.as_view(), name = 'course_edit_top'),
    path('course_edit/<int:course_pk>/', CourseEditView.as_view(), name = 'course_edit'),
    path('quiz_edit/<int:course_pk>/<int:quiz_pk>/', QuizEditView.as_view(), name = 'quiz_edit'),
    path('question_edit/<int:course_pk>/<int:quiz_pk>/<int:question_pk>/', QuestionEditView.as_view(), name = 'question_edit'),
    #Delete
    path('course_delete/<int:course_pk>/', course_delete_view, name = 'course_delete'),
    path('quiz_delete/<int:course_pk>/<int:quiz_pk>/', quiz_delete_view, name = 'quiz_delete'),
    path('question_delete/<int:course_pk>/<int:quiz_pk>/<int:question_pk>/', question_delete_view, name = 'question_delete'),
]
