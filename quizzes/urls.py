from django.urls import path
from .views.create import (
    CourseCreateView,
    QuizCreateView,
    QuestionCreateView,
)
from .views.edit import(
    CourseEditTopView,
    CourseEditView,
    QuizEditView,
    QuestionEditView,
)
from .views.search import CourseSearchView
from .views.detail import CourseDetailView
from .views.delete import(
    course_delete_view,
    quiz_delete_view,
    question_delete_view,
)
from .views.likes import LikeView

urlpatterns = [
    #Create
    path('cource_create/', CourseCreateView.as_view(), name = 'course_create'),
    path('quiz_create/<uuid:course_uuid>/', QuizCreateView.as_view(), name = 'quiz_create'),
    path('question_create/<uuid:quiz_uuid>/', QuestionCreateView.as_view(), name = 'question_create'),
    #Edit
    path('course_edit_top/<uuid:course_uuid>/', CourseEditTopView.as_view(), name = 'course_edit_top'),
    path('course_edit/<uuid:course_uuid>/', CourseEditView.as_view(), name = 'course_edit'),
    path('quiz_edit/<uuid:course_uuid>/<uuid:quiz_uuid>/', QuizEditView.as_view(), name = 'quiz_edit'),
    path('question_edit/<uuid:course_uuid>/<uuid:quiz_uuid>/<uuid:question_uuid>/', QuestionEditView.as_view(), name = 'question_edit'),
    #Delete
    path('course_delete/<uuid:course_uuid>/', course_delete_view, name = 'course_delete'),
    path('quiz_delete/<uuid:course_uuid>/<uuid:quiz_uuid>/', quiz_delete_view, name = 'quiz_delete'),
    path('question_delete/<uuid:course_uuid>/<uuid:quiz_uuid>/<uuid:question_uuid>/', question_delete_view, name = 'question_delete'),
    #Search
    path('course_search/', CourseSearchView.as_view(), name = 'course_search'),
    #Detail
    path('course_detail/<uuid:course_uuid>/', CourseDetailView.as_view(), name = 'course_detail'),

    path('course_like/<uuid:course_uuid>/', LikeView.as_view(), name='course_like'),
    
]
