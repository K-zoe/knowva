from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from answers.mixins.attempt import AnswerAttemptMixin
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
from django.db import transaction
from pprint import pprint

class AnswerAttempView(LoginRequiredMixin, AnswerAttemptMixin, View):
    template_name = 'answers/answer.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = self.get_quiz(kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session = self.check_and_get_session(self.quiz)
        question = self.get_question(session)
        if question is None:
            #NOTE: 
            return render()
        context = {'question': question}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        session = self.get_session(self.quiz)
        user_choice = request.POST.getlist('choice')
        #NOTE: session情報を前提にする。
        question_pk = session.question_order[session.current_index]
        question = Question.objects.filter(pk = question_pk).first()
        choices = Choice.objects.filter(
            question = question,
            is_correct = True
        ).values_list('pk', flat = True)

        if set(map(int, user_choice)) == set(choices):
            print('あっているよ')
            answer = Answer.objects.create(
                session = session,
                question = question,
                is_correct = True
            )
            answer.choices.add(*user_choice)

        else:
            answer = Answer.objects.create(
                session = session,
                question = question,
                is_correct = False
            )
            answer.choices.add(*user_choice)

        if session is None:
            pass
        #status = self.next_or_finish_question(session)
        return redirect()

class AnswerFeedbackView(LoginRequiredMixin, View):
    template_name = 'answer/answer_feedback.html'

    def get(self, request, *args, **kwargs):
        return 