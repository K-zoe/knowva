from django.db import models
from answers.querysets import QuizSessionQuerySet,AnswerQuerySet
import random
from quizzes.models import Question

class QuizSessionManager(models.Manager):
    def get_queryset(self):
        return QuizSessionQuerySet(self.model, using=self._db)

    def create_session(self, user, quiz):
        question_list = list(
            Question.objects.filter(
                quiz = quiz
            ).values_list('pk', flat = True)
        )
        random.shuffle(question_list)

        if not question_list:
            return None
        
        session = self.create(
            user = user,
            quiz = quiz,
            question_order = question_list
        )
        return session
    

class AnswerManager(models.Manager):
    def get_queryset(self):
        return AnswerQuerySet(self.model, using=self._db)