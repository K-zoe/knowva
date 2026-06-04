from django.db import models
from quizzes.querysets import QuizQuerySet

class QuizManager(models.Manager["Quiz"]):
    def get_queryset(self):
        return QuizQuerySet(self.model, using=self._db)