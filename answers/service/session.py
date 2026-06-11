from quizzes.models import Quiz, Question
from answers.models import QuizSession
from answers.exceptions import (
    QuizNotFoundException,
    QuestionNotFoundException,
    InvalidSessionException
)

class SessionService:
    #NOTE: Session情報の管理を行う。
    def __init__(self, course_uuid, quiz_uuid, user, ):
        self.course_uuid = course_uuid
        self.quiz_uuid = quiz_uuid
        self.user = user

    def get_quiz(self) -> Quiz:
        try:
            quiz = Quiz.objects.is_public().by_uuid(self.course_uuid, self.quiz_uuid).get()
            return quiz
        except Quiz.DoesNotExist:
            raise QuizNotFoundException('問題集が存在しません。')

    def get_session(self) -> QuizSession:
        quiz = self.get_quiz()
        return QuizSession.objects.get_session(self.user, quiz)

    def get_or_create_session(self) -> QuizSession:
        quiz = self.get_quiz()
        session = self.get_session()
        if session:
            if session.is_active is False or session.finished_at:
                session.delete()
                session = QuizSession.objects.create_session(
                    user = self.user,
                    quiz = quiz
                )
        else:
            session =  QuizSession.objects.create_session(
                    user = self.user,
                    quiz = quiz
                )

        return session
    
    def get_question(self, session) -> Question | None:
        #NOTE:session情報から次の問題を取得する。
        questions = Question.objects.filter(
            quiz = session.quiz,
            pk__in = session.question_order
        )
        if not questions:
            raise QuestionNotFoundException('問題が見つかりません。')
        question_map = {
            question.pk : question for question in questions
        }

        for idx in range(session.current_index, len(session.question_order)):
            question_id = session.question_order[idx]
            question = question_map.get(question_id)

            if question:
                if idx != session.current_index:
                    session.current_index = idx
                    session.save(update_fields=['current_index'])
                return question
        
        return None

    def check_session_finished(self, session) -> bool:
        #NOTE: sessionが終了しているかどうかを判定する。
        if session.finished_at and session.is_active is True:
            pass
        else:
            raise InvalidSessionException('有効なセッションが見つかりません。')