from django.views.generic import View, UpdateView
from ..models import Course,Quiz,Question,Choice
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from ..forms import (
    CourseForm,
    QuizEditForm,
    QuestionForm,
    ChoiceForm
)
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.db import transaction
from django.core.paginator import Paginator

class CourseEditTopView(LoginRequiredMixin, View):
    template_name = 'quizzes/course_edit_top.html'

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(
            Course,
            user = self.request.user,
            uuid = kwargs.get('course_uuid')
        )
        quizzes = Quiz.objects.filter(course = course).all()
        context = {'course':course, 'quizzes':quizzes}
        return render(request, self.template_name, context)

class CourseEditView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'quizzes/course_edit.html'

    def get_object(self):
        queryset = get_object_or_404(
            Course,
            user = self.request.user,
            uuid = self.kwargs.get('course_uuid')
        )
        return queryset
    
    def get_success_url(self):
        return reverse(
            'course_edit_top',
            kwargs = {'course_uuid': self.kwargs.get('course_uuid')}
        )
    
class QuizEditView(LoginRequiredMixin, UpdateView):
    model = Quiz
    form_class = QuizEditForm
    template_name = 'quizzes/quiz_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = Question.objects.filter(
            quiz = self.get_object()
        ).order_by('pk')
        p = Paginator(object, 10)
        page_obj = p.get_page(self.request.GET.get('page'))
        context['page_obj'] = page_obj
        context['page_obj_count'] = p.count
        context['questions'] = page_obj.object_list
        return context

    def get_object(self):
        course = get_object_or_404(
            Course,
            user = self.request.user,
            uuid = self.kwargs.get('course_uuid')
        )
        quiz = get_object_or_404(
            Quiz,
            course = course,
            uuid = self.kwargs.get('quiz_uuid')
        )
        return quiz
    
    def form_valid(self, form):
        is_public = form.cleaned_data['is_public']
        
        if is_public is False:
            #TODO: ユーザーの回答状況をリセット
            pass
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
            'quiz_edit',
            kwargs = {
                'course_uuid': self.kwargs.get('course_uuid'),
                'quiz_uuid': self.kwargs.get('quiz_uuid')
            }
        )

class QuestionEditView(LoginRequiredMixin, View):
    template_name = 'quizzes/question_edit.html'
    form = QuestionForm
    formset = inlineformset_factory(
        Question,
        Choice,
        form = ChoiceForm,
        extra = 0,
        can_delete = True
    )

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(
            Course,
            user = request.user,
            uuid = kwargs.get('course_uuid')
        )
        quiz = get_object_or_404(
            Quiz,
            course = course,
            uuid = kwargs.get('quiz_uuid'),
            is_public = False
        )
        question = get_object_or_404(
            Question,
            quiz = quiz,
            uuid = kwargs.get('question_uuid')
        )

        form = self.form(instance = question)
        choice_formset = self.formset(instance = question)

        context = {
            'form': form,
            'choice_formset': choice_formset,
            'course': course,
            'quiz': quiz
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(
            Course,
            user=request.user,
            uuid=kwargs.get('course_uuid'),
        )
        quiz = get_object_or_404(
            Quiz,
            course=course,
            uuid=kwargs.get('quiz_uuid'),
            is_public = False
        )
        question = get_object_or_404(
            Question,
            quiz=quiz,
            uuid=kwargs.get('question_uuid')
        )

        form = self.form(request.POST, instance=question)
        choice_formset = self.formset(
            request.POST,
            instance=question
        )

        if form.is_valid() and choice_formset.is_valid():
            with transaction.atomic():
                form.save()
                choice_formset.save()

            return HttpResponseRedirect(
                reverse('quiz_edit', kwargs={
                    'course_uuid': course.uuid,
                    'quiz_uuid': quiz.uuid
                })
            )

        else:
            context = {
                'form': form,
                'choice_formset': choice_formset,
                'course': course,
                'quiz': quiz
            }
            return render(request, self.template_name, context)