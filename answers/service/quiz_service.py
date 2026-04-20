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

class QuizSessionService:
    #NOTE: Session情報の管理を行う。
    def __init__(self, user, quiz):
        self.user = user
        self.quiz = quiz
    
    def get_session(self) -> QuizSession:
        session = QuizSession.objects.filter(
            user = self.user,
            quiz = self.quiz,
        ).first()
        return session
    
    def create_session(self) -> QuizSession | None:
        question_list = list(
            Question.objects.filter(
                quiz = self.quiz
            ).values_list('pk', flat = True)
        )
        random.shuffle(question_list)

        if not question_list:
            return None
        
        session = QuizSession.objects.create(
            user = self.user,
            quiz = self.quiz,
            question_order = question_list
        )
        return session
    
    def delete_session(self, session) -> None:
        session.delete()

    def get_or_create_session(self) -> QuizSession:
        #NOTE: sessionの状態に合わせて、取得、作成、再作成して返す。
        session = self.get_session()
        if session:
            if session.is_active is False or session.finished_at:
                #再挑戦。
                self.delete_session(session)
                session = self.create_session()
        else:
            session = self.create_session()

        return session
    
    def next_or_finish_question(self, session) -> None:
        #NOTE: sessionの状態を更新する。次の問題に進むか、終了させるか。
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

    def get_prev_index(self, url_index) -> int | None:
        if url_index == 0:
            return None
        
        elif url_index > 0:
            return url_index -1

    def get_next_index(self, session, url_index, current_index) -> int | None:
        #url_indexが現在のindexで、かつsessionが終了している場合はNone
        if url_index == current_index and session.finished_at:
            return None
        #url_indexに1足したindexが現在のindexで、かつsessionが終了していない場合はNone
        elif url_index + 1 == current_index and session.finished_at is None:
            return None
        #url_indexが現在のindexより小さく。
        elif url_index < current_index and url_index >= 0:
            return url_index + 1
        
        else:
            return None
    
    def get_question(self, session) -> Question | None:
        #NOTE:session情報から次の問題を取得する。
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

    def check_answer(self, session, user_choice) -> Answer | None:
        #NOTE: 回答の正誤を判定して保存する。
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
            return answer
        
        except IntegrityError:
            return None
