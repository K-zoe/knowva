from django.db import models
import uuid
from quizzes.managers import QuizManager

class Course(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, unique = True)
    title = models.CharField(max_length = 100)
    tag = models.CharField(max_length = 200)
    user = models.ForeignKey('accounts.User', on_delete = models.CASCADE, related_name = 'course')
    description = models.TextField(blank = True, null = True)
    is_public = models.BooleanField(default=False)
    like_count = models.PositiveIntegerField(default = 0)

class Quiz(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, unique = True)
    course = models.ForeignKey('Course', on_delete = models.CASCADE, related_name = 'quiz')
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_public = models.BooleanField(default = False)

    objects = QuizManager()


class Question(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, unique = True)
    quiz = models.ForeignKey('Quiz', on_delete = models.CASCADE, related_name = 'question')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    explanation = models.TextField(blank = True, null = True)

class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete = models.CASCADE, related_name = 'choice')
    text = models.TextField()
    explanation = models.TextField(blank=True, null = True)
    is_correct = models.BooleanField(default = False)
    

class Like(models.Model):
    user = models.ForeignKey('accounts.User', on_delete = models.CASCADE, related_name = 'like')
    course = models.ForeignKey('Course', on_delete = models.CASCADE, related_name = 'like')

    class Meta:
        unique_together = ('user', 'course')