from django.views.decorators.http import require_POST
from ..models import Course,Quiz,Question
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

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

@require_POST
def question_delete_view(request, *args, **kwargs):
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
    question = get_object_or_404(
        Question,
        quiz = quiz,
        pk = kwargs.get('question_pk')
    )
    question.delete()

    return HttpResponseRedirect(
        reverse('quiz_edit', kwargs = {
            'course_pk': course.pk,
            'quiz_pk': quiz.pk
        })
    )