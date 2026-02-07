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
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.db import transaction

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
        can_delete = True
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
        if self.request.method == 'POST':
            context['choice_formset'] = self.choice_formset(self.request.POST)
        else:
            context['choice_formset'] = self.choice_formset()
        return context
    
    def get_success_url(self):
        return reverse(
            'question_create',
            kwargs = {'quiz_id': self.quiz.pk}
        )

    def form_valid(self, form):
        #TODO: formsetのバリデーションと、quizの保存処理を追加する。
        form.instance.quiz = self.quiz
        question = form.save(commit=False)
        formset = self.choice_formset(self.request.POST, instance = question)

        if not formset.is_valid():
            return self.formset_invalid(formset)
        else:
            #NOTE: トランザクション処理
            with transaction.atomic():
                question.save()
                formset.save()
        #NOTE: ボタンによって画面遷移先を変更する。
        action = self.request.POST.get("action")
        
        if action == "next":
            return HttpResponseRedirect(self.get_success_url())
        else:
            #TODO: リダイレクト先の画面を作成した後に実装する。
            return HttpResponseRedirect()
        
    def formset_invalid(self, form):
        context = self.get_context_data(form = form)
        return self.render_to_response(context)