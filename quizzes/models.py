from django.db import models

class Course(models.Model):
    title = models.CharField(max_length = 100)
    tag = models.CharField(max_length = 200)
    user = models.ForeignKey('accounts.User', on_delete = models.CASCADE, related_name = 'course')
    description = models.TextField(blank = True, null = True)
    is_public = models.BooleanField(default=False)

class Quiz(models.Model):
    course = models.ForeignKey('Course', on_delete = models.CASCADE, related_name = 'quiz')
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_public = models.BooleanField(default = True)


class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete = models.CASCADE, related_name = 'question')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    explanation = models.TextField(blank = True, null = True)

class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete = models.CASCADE, related_name = 'choice')
    text = models.TextField()
    explanation = models.TextField(blank=True, null = True)
    is_correct = models.BooleanField(default = False)
    