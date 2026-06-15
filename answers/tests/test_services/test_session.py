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

    def test__get_session_correct(self):
        self.create_course_quize_question()
        create_session = self.create_session(self.quiz)
        session_serivce = SessionService(
            self.course.uuid,
            self.quiz.uuid,
            self.user
        )
        print(f'a:{create_session}')
        session = session_serivce.get_session()
        print(f'b:{session}')
        self.assertEqual(session,create_session)