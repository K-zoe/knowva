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
        session = self.session_check(self.quiz)
        question = self.get_question(session)
        
        return render()

class AnswerStartView(LoginRequiredMixin, AnswerAttemptMixin, View):
    template_name = 'answers/answer.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.quiz = self.get_quiz(kwargs)
        self.session = self.get_session(request, self.quiz)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.session:
            if self.session.finished_at:
                #NOTE: 完了後の場合は再挑戦。※不正な操作扱いでもいいかも？
                return redirect()
            else:
                #NOTE: 途中の場合は再開。
                return redirect('answer_resume', kwargs.get('course_pk'), kwargs.get('quiz_pk'))
                    
        with transaction.atomic():
            #NOTE: 問題がないのにsessionだけが作成されるのを防ぐ。
            session = self.create_session(request, self.quiz)
            question = get_object_or_404(
                Question,
                pk = session.question_order[session.current_index],
                quiz = self.quiz
            )

        context = {'question': question}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.session is None or self.session.finished_at is not None:
            #NOTE: 不正な操作にする。
            return redirect()
        
        #TODO: 正解チェック処理作成。
        
        return redirect()

class AnswerFeedbackView(LoginRequiredMixin, View):
    template_name = 'answer/answer_feedback.html'

    def get(self, request, *args, **kwargs):
        pass