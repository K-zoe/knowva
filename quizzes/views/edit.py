from django.views.generic import CreateView, View, UpdateView
from django.views.decorators.http import require_POST
from ..models import Course,Quiz,Question,Choice
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404, render
from ..forms import (
    CourseForm,
    QuizForm,
    QuestionForm,
    ChoiceForm
)
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.db import transaction


class CourseEditTopView(LoginRequiredMixin, View):
    template_name = 'quizzes/course_edit_top.html'

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(
            Course,
            user = self.request.user,
            pk = kwargs.get('course_pk')
        )
        quizzes = Quiz.objects.filter(course = course).all()
        context = {'course':course, 'quizzes':quizzes}
        return render(request, self.template_name, context)

@require_POST
def course_delete_view(request, *args, **kwargs):
    course = get_object_or_404(
        Course,
        user = request.user,
        pk = kwargs.get('course_pk')
    )
    course.delete()

    return HttpResponseRedirect(reverse('my_created_courses'))

@require_POST
def quiz_delete_view(request, *args, **kwargs):
    course = get_object_or_404(
        Course,
        user = request.user,
        pk = kwargs.get('course_pk')
    )
    quiz = get_object_or_404(
        Quiz,
        course = course,
        pk = kwargs.get('quiz_pk')
    )
    quiz.delete()

    return HttpResponseRedirect(
        reverse('course_edit_top', kwargs = {'course_pk': course.pk})
        )


class CourseEditView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'quizzes/course_edit.html'

    def get_object(self):
        queryset = get_object_or_404(
            Course,
            user = self.request.user,
            pk = self.kwargs.get('course_pk')
        )
        return queryset
    
    def get_success_url(self):
        return reverse(
            'course_edit_top',
            kwargs = {'course_pk': self.kwargs.get('course_pk')}
        )
    
class QuizEditView(LoginRequiredMixin, UpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quizzes/quiz_edit.html'

    def get_context_data(self, **kwargs):
        #TODO: 問題集の編集画面で問題の一覧を表示する。
        context = super().get_context_data(**kwargs)
        return context
        pass

    def get_object(self):
        course = get_object_or_404(
            Course,
            user = self.request.user,
            pk = self.kwargs.get('course_pk')
        )
        quiz = get_object_or_404(
            Quiz,
            course = course,
            pk = self.kwargs.get('quiz_pk')
        )
        return quiz
    
    def get_success_url(self):
        return reverse(
            'quiz_edit',
            kwargs = {
                'course_pk': self.kwargs.get('course_pk'),
                'quiz_pk': self.kwargs.get('quiz_pk')
            }
        )