from django.shortcuts import render,get_object_or_404
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

    def get_session(self,quiz) -> QuizSession:
        session = QuizSession.objects.filter(
            user = self.request.user,
            quiz = quiz,
        ).first()
        return session
    
    def create_session(self, quiz) -> QuizSession:
        #TODO:quizの登録だけでquiestionがない可能性があるので対応が必要
        question_list = list(
            Question.objects.filter(
                quiz = quiz
            ).values_list('pk', flat = True)
        )
        random.shuffle(question_list)

        session = QuizSession.objects.create(
            user = self.request.user,
            quiz = quiz,
            question_order = question_list
        )
        return session
    
    def delete_session(self, session_pk):
        QuizSession.objects.filter(
            pk = session_pk,
            user = self.request.user
        ).delete()

    def session_check(self, quiz):
        session = self.get_session(quiz)
        if session:
            if session.is_active is False or session.finished_at:
                #再挑戦。
                self.delete_session(session.pk)
                session = self.create_session(quiz)
        else:
            session = self.create_session(quiz)


        return session

    def get_quiz(self, kwargs) -> Quiz:
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
    
    def get_question(self, session) -> Question | None:
        for idx in range(session.current_index, len(session.question_order)):
            question = Question.objects.filter(
                pk=session.question_order[idx],
                quiz= session.quiz
            ).first()

            if question:
                if idx != session.current_index:
                    session.current_index = idx
                    session.save(update_fields=['current_index'])
                return question

        return None