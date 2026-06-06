from quizzes.models import Quiz
from answers.models import QuizSession

class SessionService:
    #NOTE: Session情報の管理を行う。
    def __init__(self, course_uuid, quiz_uuid, user, ):
        self.course_uuid = course_uuid
        self.quiz_uuid = quiz_uuid
        self.user = user

    def get_or_create_session(self) -> QuizSession:
        quiz = Quiz.objects.is_public().by_uuid(self.course_uuid, self.quiz_uuid)
        if quiz is None:
            raise ValueError
        
        session = QuizSession.objects.get_session(self.user, quiz)
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

    def check_session_finished(self, session) -> bool:
        #NOTE: sessionが終了しているかどうかを判定する。
        if session.finished_at and session.is_active is True:
            return True
        else:
            return False