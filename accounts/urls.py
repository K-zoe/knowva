from django.urls import path,include
from .views import (
    SignupPageView,
    LoginPageView,
    LogoutPageView,
    CurrentCoursesView,
    MyCreatedCoursesView,
    ProfileEditView
)

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name = 'signup'),
    path('login/', LoginPageView.as_view(), name = 'login'),
    path('logout/', LogoutPageView.as_view(), name = 'logout'),
    path('mypage/', CurrentCoursesView.as_view(), name = 'mypage_current_courses'),
    path('my_created_courses/', MyCreatedCoursesView.as_view(), name = 'my_created_courses'),

    path('profile_edit/', ProfileEditView.as_view(), name = 'profile_edit'),
]
