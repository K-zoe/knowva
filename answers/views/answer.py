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
import random
from django.db import transaction
from pprint import pprint

class AnswerAttemptMixin:
    #NOTE:　使いまわす機能はMixinにしておく

    def get_session(self, request, quiz) -> QuizSession:
        session = QuizSession.objects.filter(
            user = request.user,
            quiz = quiz,
        ).first()
        return session
    
    def create_session(self, request, quiz):
        question_list = list(
            Question.objects.filter(
                quiz = quiz
            ).values_list('pk', flat = True)
        )
        random.shuffle(question_list)

        session = QuizSession.objects.create(
            user = request.user,
            quiz = quiz,
            question_order = question_list
        )
        return session
    
    def delete_session(self, request, session_pk):
        QuizSession.objects.delete(
            pk = session_pk,
            user = request.user
        )

    def get_quiz(self, kwargs) -> Question:
        #NOTE: 公開フラグが有効になっているものだけを返す。
        course = get_object_or_404(
            Course,
            pk = kwargs.get('course_pk'),
            is_public = True
        )
        quiz = get_object_or_404(
            Quiz,
            course = course,
            pk = kwargs.get('quiz_pk'),
            is_public = True
        )
        return quiz
    
    def get_question(self, session, quiz):
        question_ids = session.question_order[session.current_index:]

        questions = {
            q.id: q
            for q in Question.objects.filter(
                id__in=question_ids,
                quiz=quiz
            )
        }

        return next(
            (questions[pk] for pk in question_ids if pk in questions),
            None
        )



class AnswerStartView(LoginRequiredMixin, AnswerAttemptMixin, View):
    template_name = 'answers/answer.html'
    
    def get(self, request, *args, **kwargs):
        quiz = self.get_quiz(kwargs)
        session = self.get_session(request, quiz)
        
        if session:
            if session.finished_at:
                #NOTE: 完了後の場合は再挑戦。※不正な操作扱いでもいいかも？
                return redirect()
            else:
                #NOTE: 途中の場合は再開。
                return redirect('answer_resume', kwargs.get('course_pk'), kwargs.get('quiz_pk'))
        
        with transaction.atomic():
            #NOTE: 問題がないのにsessionだけが作成されるのを防ぐ。
            session = self.create_session(request, quiz)
            question = get_object_or_404(
                Question,
                pk = session.question_order[session.current_index],
                quiz = quiz
            )

        context = {'question': question}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect()
    
class AnswerResumeView(LoginRequiredMixin, AnswerAttemptMixin, View):
    template_name = 'answers/answer.html'

    def get(self, request, *args, **kwargs):
        quiz = self.get_quiz(kwargs)
        session = self.get_session(request, quiz)
        
        if not session:
            return redirect('answer_start', kwargs.get('course_pk'), kwargs.get('quiz_pk'))
        
        elif session.finished_at:
            #NOTE: 完了後の場合は再挑戦。※不正な操作扱いでもいいかも？
            return redirect()

        question = self.get_question(session = session, quiz = quiz)

        if question is None:
            #NOTE: 問題がなければ完了にして終了。
            print('データなし')

        context = {'question': question}
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect()
        

class AnswerRetryWrongView(LoginRequiredMixin, AnswerAttemptMixin, View):
    template_name = 'answer/answer.html'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class AnswerFinishView(LoginRequiredMixin, AnswerAttemptMixin, View):
    template_name = ''

    def get(self, request, *args, **kwargs):
        pass

class AnswerAttemptView(LoginRequiredMixin, AnswerAttemptMixin, View):
    template_name = 'answer/answer.html'

    def get(self, request, *args, **kwargs):
        quiz = self.get_quiz(kwargs)
        session = self.get_session(request, quiz)

        if session:
            if session.finished_at:
                #NOTE: 完了後の場合は再挑戦。
                return redirect()
            else:
                #NOTE: 途中の場合は再開。
                return redirect()

    def post(self, request, *args, **kwargs):
        pass



class AnswerFeedbackView(LoginRequiredMixin, View):
    template_name = 'answer/answer_feedback.html'

    def get(self, request, *args, **kwargs):
        pass