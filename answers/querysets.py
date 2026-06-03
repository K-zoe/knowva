from django.db import models

class QuizSessionQuerySet(models.QuerySet):
    def get_session(self, user, quiz):
        return self.filter(
            user = user,
            quiz = quiz,
            is_active = True
        ).first()

class AnswerQuerySet(models.QuerySet):
    def calculate_score(self, session):
        #TODO: total=len(session.question_order)はサービスに移す
        total = len(session.question_order)
        correct = self.filter(
            session = session,
            is_correct = True
        ).count()

        return {'total': total, 'correct': correct}