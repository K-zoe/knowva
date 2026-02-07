from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,View
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm,LoginForm,UserForm,ProfileForm
from django.contrib.auth import login,authenticate
from accounts.models import Profile,User
from quizzes.models import Course
from django.db import transaction
from django.views.csrf import csrf_failure

def csrf_failure(request, reason = ""):
    """CSRF検証失敗時の画面"""
    template_name = 'accounts/csrf_error.html'
    return render(request, template_name, status = 403)

class SignupPageView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('mypage_current_courses')

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
    next_page = reverse_lazy('mypage_current_courses')

class LogoutPageView(LogoutView):
    next_page = reverse_lazy('login')

class CurrentCoursesView(LoginRequiredMixin, ListView):
    #マイページを開いた最初の表示
    #model = ''#TODO: 解いている問題を表示するようにする。
    template_name = 'accounts/current_courses.html'
    paginate_by = None #TODO: ページネーション機能を追加

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        #TODO: 解いている問題のリスト作成が完了したら、修正する。
        return None#super().get_queryset()
    
class MyCreatedCoursesView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'accounts/my_created_courses.html'
    paginate_by = 2
    ordering = ['-pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user = self.request.user)

class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_edit.html'

    def get(self, request):
        user_form = UserForm(instance = request.user)
        profile_form = ProfileForm(instance = request.user.profile)

        context = {'user_form':user_form, 'profile_form':profile_form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = ProfileForm(request.POST, instance = request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()

                return redirect('mypage_current_courses')
        else:
            context = {'user_form':user_form, 'profile_form':profile_form}
            return render(request, self.template_name, context)