from __future__ import annotations
from typing import TYPE_CHECKING
from django.db import models

if TYPE_CHECKING:
    from accounts.models import User
    from quizzes.models import Quiz
    from answers.models import QuizSession,Answer

class QuizSessionQuerySet(models.QuerySet):
    def get_session(self, user: 'User' , quiz: 'Quiz') -> QuizSession | None:
        return self.filter(
            user = user,
            quiz = quiz,
            is_active = True
        ).first()

class AnswerQuerySet(models.QuerySet):
    def for_feedback(self):
        return self.select_related(
            'question'
        ).prefetch_related(
            'question__choice',
            'choices'
        )

    def by_session_and_question(self, session, question_pk):
        return self.get(
            session=session,
            question_id=question_pk
        )

    def calculate_score(self, session: 'QuizSession'):
        return self.filter(
            session = session,
            is_correct = True
        ).count()