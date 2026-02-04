from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm,LoginForm
from django.contrib.auth import login,authenticate
from .models import Profile
from django.db import transaction
from django.views.csrf import csrf_failure

def csrf_failure(request, reason = ""):
    """CSRF検証失敗時の画面"""
    template_name = 'accounts/csrf_error.html'
    return render(request, template_name, status = 403)

class SignupPageView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('mypage')

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            Profile.objects.create(
                user = self.object,
                biography = "よろしくお願いします。"
            )

        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())

class LoginPageView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    next_page = reverse_lazy('mypage')

class LogoutPageView(LogoutView):
    next_page = reverse_lazy('login')

class MyPageView(LoginRequiredMixin, ListView):
    #model = ''#TODO: 解いている問題を表示するようにする。
    template_name = 'accounts/mypage.html'
    paginate_by = None #TODO: ページネーション機能を追加

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        #TODO: 解いている問題のリスト作成が完了したら、修正する。
        return None#super().get_queryset()