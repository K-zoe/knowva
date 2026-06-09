from answers.models import Answer

class ResultService:
    def __init__(self, session):
        self.session = session
        
    def calculate_score(self) -> dict:
        #NOTE: 全問中何問正解したかを返す。
        total = len(self.session.question_order)
        correct = Answer.objects.calculate_score(self.session)

        return {'total': total, 'correct': correct}