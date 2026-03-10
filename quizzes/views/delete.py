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
        uuid = kwargs.get('course_uuid')
    )
    course.delete()

    return HttpResponseRedirect(reverse('my_created_courses'))

@require_POST
def quiz_delete_view(request, *args, **kwargs):
    course = get_object_or_404(
        Course,
        user = request.user,
        uuid = kwargs.get('course_uuid')
    )
    quiz = get_object_or_404(
        Quiz,
        course = course,
        uuid = kwargs.get('quiz_uuid')
    )
    quiz.delete()

    return HttpResponseRedirect(
        reverse('course_edit_top', kwargs = {'course_uuid': course.uuid})
        )

@require_POST
def question_delete_view(request, *args, **kwargs):
    course = get_object_or_404(
        Course,
        user = request.user,
        uuid = kwargs.get('course_uuid')
    )
    quiz = get_object_or_404(
        Quiz,
        course = course,
        uuid = kwargs.get('quiz_uuid')
    )
    question = get_object_or_404(
        Question,
        quiz = quiz,
        uuid = kwargs.get('question_uuid')
    )
    question.delete()

    return HttpResponseRedirect(
        reverse('quiz_edit', kwargs = {
            'course_uuid': course.uuid,
            'quiz_uuid': quiz.uuid
        })
    )