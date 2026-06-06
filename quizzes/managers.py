from django.db import models
from quizzes.querysets import QuizQuerySet

class QuizManager(models.Manager.from_queryset(QuizQuerySet)):
    pass