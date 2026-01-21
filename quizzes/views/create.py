from django.views.generic import CreateView
from quizzes.models import Course,Quiz,Question
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'tag', 'discription', 'is_public']
    template_name = 'quizzes/course_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
            'quiz_create',
            kwargs = {'course_id': self.object.pk}
        )

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = ['title', 'discription', 'is_public']
    template_name = 'quizzes/quiz_create.html'

    def dispatch(self, request, *args, **kwargs):
        #NOTE:後々、この処理がほかのクラスでも出るのであればベースクラスの作成を検討
        self.course = get_object_or_404(
            Course,
            pk = kwargs.get('course_id'),
            user = self.request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
            'question_create',
            kwargs = {'quiz_id': self.object.pk}
        )
    
#TODO: QuestionCreateViewの作成。問題と質問を同時に作成できるようにするかそれとも別々にするか悩むなー
class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'text', 'explanation']
    template_name = 'quizzes/question_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(
            Quiz,
            pk = kwargs.get('quiz_id'),
            course__user = self.request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.quiz = self.quiz
        return super().form_valid(form)