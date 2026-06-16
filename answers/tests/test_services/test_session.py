from test.base import BaseTest
from answers.service.session import SessionService
from answers.models import QuizSession

class SessionServiceTest(BaseTest):
    def create_course_quize_question(self):
        self.course = self.course_create()
        self.quiz = self.quiz_create(self.course)
        self.question = self.question_create(self.quiz)
        self.choice1_create(self.question)
        self.choice2_create(self.question)

    def create_session(self, quiz):
        session = QuizSession.objects.create_session(
            user = self.user,
            quiz = quiz
        )

        return session

    def test_get_session_success(self):
        self.create_course_quize_question()
        create_session = self.create_session(self.quiz)
        session_serivce = SessionService(
            self.course.uuid,
            self.quiz.uuid,
            self.user
        )
        
        session = session_serivce.get_session()
        self.assertEqual(session,create_session)

    def test_get_or_create_session_success(self):
        self.create_course_quize_question()
        session_serivce = SessionService(
            self.course.uuid,
            self.quiz.uuid,
            self.user
        )
        session = session_serivce.get_or_create_session()
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.quiz.uuid, self.quiz.uuid)
