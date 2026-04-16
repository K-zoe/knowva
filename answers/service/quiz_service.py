from django.shortcuts import get_object_or_404
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
from django.db import IntegrityError

class QuizService:
    #NOTE: クイズセッションの管理を行う。
    @staticmethod
    def get_session(user,quiz) -> QuizSession:
        session = QuizSession.objects.filter(
            user = user,
            quiz = quiz,
        ).first()
        return session
    
    @staticmethod
    def create_session(user,quiz) -> QuizSession:
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
            user = user,
            quiz = quiz,
            question_order = question_list
        )
        return session
    
    @staticmethod
    def delete_session(user, session_pk):
        QuizSession.objects.filter(
            pk = session_pk,
            user = user
        ).delete()

    @staticmethod
    def check_and_get_session(user, quiz):
        session = QuizService.get_session(user, quiz)
        if session:
            if session.is_active is False or session.finished_at:
                #再挑戦。
                QuizService.delete_session(user, session.pk)
                session = QuizService.create_session(user, quiz)
        else:
            session = QuizService.create_session(user, quiz)

        return session
    
    @staticmethod
    def next_or_finish_question(session):
        current_index = session.current_index + 1
        
        total = len(session.question_order)

        if current_index >= total:
            session.finished_at = timezone.now()
            session.save(update_fields = [
                'finished_at'
            ])
        else:
            session.current_index+=1
            session.save(update_fields = ['current_index'])

    @staticmethod
    def get_prev_index(url_index):
        if url_index == 0:
            return None
        
        elif url_index > 0:
            return url_index -1

    @staticmethod
    def get_next_index(session, url_index, current_index):

        if url_index == current_index and session.finished_at:
            return None
        
        elif url_index + 1 == current_index and session.finished_at is None:
            return None

        elif url_index < current_index and url_index >= 0:
            return url_index + 1
        
        else:
            return None
    
    @staticmethod
    def get_quiz(course_uuid, quiz_uuid) -> Quiz:
        #NOTE: 公開フラグが有効になっているものだけを返す。
        course = get_object_or_404(
            Course,
            uuid = course_uuid,
            is_public = True
        )
        quiz = get_object_or_404(
            Quiz,
            course = course,
            uuid = quiz_uuid,
            is_public = True
        )
        return quiz
    
    @staticmethod
    def get_question(session) -> Question | None:
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

    @staticmethod
    def check_answer(session, user_choice):
        question_pk = session.question_order[session.current_index]
        question = Question.objects.filter(pk = question_pk).first()
        choices = Choice.objects.filter(
            question = question,
            is_correct = True
        ).values_list('pk', flat = True)

        if set(map(int, user_choice)) == set(choices):
            is_correct = True
        else:
            is_correct = False
        
        try:
            answer = Answer.objects.create(
                session = session,
                question = question,
                is_correct = is_correct
            )
            answer.choices.add(*user_choice)
        except IntegrityError:
            raise ValueError("不正な操作")