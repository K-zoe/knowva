from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from quizzes.models import (
    Course,
    Quiz,
    Question,
    Choice
)
from answers.models import(
    QuizSession,
    Answer
)

class AnswerAttemptMixin:
    #NOTE:　使いまわす機能はMixinにしておく
    template_name = 'answer/answer.html'

    def get_or_create_session(self, request, **kwargs) -> QuizSession:
        session = QuizSession.objects.get_or_create(
            user = request.user,
            quiz = kwargs.get('quiz_pk')
        )
        return session
    
    def delete_session(self, request, session_pk):
        QuizSession.objects.delete(
            pk = session_pk,
            user = request.user
        )

    def get_question(self, **kwargs) -> Question:
        course = get_object_or_404(
            Course,
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
        return question

class AnswerStartView(
    LoginRequiredMixin,
    AnswerAttemptMixin,
    View
):

    def get(self, request, *args, **kwargs):
        question = self.get_question(kwargs)
        session = self.get_or_create_session(request, kwargs)
            

        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect()
    
class AnswerResumeView(
    LoginRequiredMixin,
    AnswerAttemptMixin,
    View
):
    def get(self, request, *args, **kwargs):
        session = self.get_or_create_session(request, kwargs)

        context = {}

    def post(self, request, *args, **kwargs):
        return redirect()
        

class AnswerRetryWrongView(
    LoginRequiredMixin,
    AnswerAttemptMixin,
    View
):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass



class AnswerFeedbackView(LoginRequiredMixin, View):
    template_name = 'answer/answer_feedback.html'

    def get(self, request, *args, **kwargs):
        pass