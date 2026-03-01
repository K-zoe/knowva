from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from quizzes.models import (
    Course,
    Quiz,
    Question,
    Choice
)

class CourseQuizListView(View):
    #NOTE:　ここまではアカウントを作成していないユーザーでもアクセスできる。
    template_name = 'answers/course_quiz_list.html'

    def get(self, request, *args, **kwargs):
        #TODO: 回答済みのクイズは成果率と再挑戦ボタンを表示。回答機能を作成した後に実装する。
        #TODO: 未回答のクイズは、挑戦ボタンを表示。
        course = get_object_or_404(
            Course,
            pk = kwargs.get('course_pk')
        )
        quizzes = Quiz.objects.filter(course = course).all()

        context ={'course': course, 'quizzes': quizzes}

        return render(request, self.template_name, context)
