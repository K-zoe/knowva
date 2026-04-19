from quizzes.models import(
    Course,
    Quiz,
    Question,
    Choice
)


class QuizMixin:
    #NOTE: URLパラメーターから取得取得するものはここで処理する。
    def get_quiz(self,course_uuid, quiz_uuid) -> Quiz:
        #NOTE: 公開フラグが有効になっているものだけを返す。
        course = Course.objects.filter(
            uuid = course_uuid,
            is_public = True
        ).first()

        quiz = Quiz.objects.filter(
            course = course,
            uuid = quiz_uuid,
            is_public = True
        ).first()

        return quiz
    
