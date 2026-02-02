from django.urls import path,include
from .views import (
    SignupPageView,
    LoginPageView,
    LogoutPageView,
    MyPageView,
)

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name = 'signup'),
    path('login/', LoginPageView.as_view(), name = 'login'),
    path('logout/', LogoutPageView.as_view(), name = 'logout'),
    path('mypage/', MyPageView.as_view(), name = 'mypage'),
]
