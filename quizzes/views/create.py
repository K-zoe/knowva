from django.views.generic import CreateView
from quizzes.models import Course,Quiz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'tag', 'discription', 'is_public']
    template_name = 'quizzes/course_create.html'
    #TODO:QuizCreateViewのURLに「course_id」を渡すように修正する。
    success_url = reverse_lazy('quiz_create')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['title', 'discription', 'is_public']
    template_name = 'quizzes/quiz_create.html'
    success_url = reverse_lazy('')

    def dispatch(self, request, *args, **kwargs):
        #NOTE:後々、この処理がほかのクラスでも出るのであればベースクラスの作成を検討
        self.course = get_object_or_404(
            Course,
            course = kwargs.get('course_id'),
            user = self.request.user
        )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)