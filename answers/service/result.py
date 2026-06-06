from answers.models import Answer

class AnswerService:
    def __init__(self, user, quiz):
        self.user = user
        self.quiz = quiz
        
    def calculate_score(self, session) -> dict:
        #NOTE: 全問中何問正解したかを返す。
        total = len(session.question_order)
        correct = Answer.objects.filter(
            session = session,
            is_correct = True
        ).count()

        return {'total': total, 'correct': correct}