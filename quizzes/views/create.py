from django.views.generic import CreateView
from ..models import Course,Quiz,Question,Choice
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from ..forms import (
    CourseForm,
    QuizForm,
    QuestionForm,
    ChoiceForm
)
from django.forms import inlineformset_factory

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
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
    form_class = QuizForm
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
    
class QuestionCreateView(LoginRequiredMixin, CreateView):
    #NOTE: QuestionとChoiceを同時に作成できるようにしている。
    model = Question
    form_class = QuestionForm
    template_name = 'quizzes/question_create.html'
    #NOTE: Choiceは複数作成できるようにinlineformsetを採用
    choice_formset = inlineformset_factory(
        Question,
        Choice,
        form = ChoiceForm,
        extra = 2,
        can_delete = False
    )

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(
            Quiz,
            pk = kwargs.get('quiz_id'),
            course__user = self.request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        #TODO: POST時のformsetも対応させる。
        context = super().get_context_data(**kwargs)
        context['choice_formset'] = self.choice_formset()
        return context

    def form_valid(self, form):
        form.instance.quiz = self.quiz
        return super().form_valid(form)