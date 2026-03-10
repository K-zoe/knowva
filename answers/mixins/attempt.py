from django.shortcuts import render,get_object_or_404
from quizzes.models import (
    Course,
    Quiz,
    Question,
    Choice
)
from django.utils import timezone
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

        if not question_list:
            #NOTE: questionがない場合は回答ボタンを表示させないようにするが、念のため
            raise ValueError('このクイズには問題がありません。')
        
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

    def check_and_get_session(self, quiz):
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
            uuid = kwargs.get('course_uuid'),
            is_public = True
        )
        print("a")
        quiz = get_object_or_404(
            Quiz,
            course = course,
            uuid = kwargs.get('quiz_uuid'),
            is_public = True
        )
        print("b")
        return quiz
    
    def get_question(self, session) -> Question | None:
        #NOTE:問題表示の取得時だけ使用する。回答時の取得は別に用意する。
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
    
    def next_or_finish_question(self, session):
        session.current_index +=1
        
        total = len(session.question_order)

        if session.current_index >= total:
            session.finished_at = timezone.now()
            session.save(update_fields = [
                'current_index',
                'finished_at'
            ])
        else:
            session.save(update_fields = ['current_index'])


class AnswerCheckMixin:
    #NOTE:　回答チェック
    
    def check_answer(self, session, choice):
        session.question_order
        quiz_list = list(
            Question.objects.filter(
                quiz = session.quiz
            ).values_list('pk', flat = True)
        )
        question_pk = quiz_list[session.current_index]
        Choice.objects.filter()


        
        return