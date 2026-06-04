from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from answers.managers import QuizSessionManager, AnswerManager

class QuizSession(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE, related_name='sessions')
    question_order = JSONField(null=True, blank=True)# ランダム出題順を保存（SQLite なので JSONField）
    current_index = models.IntegerField(default=0)# 現在の問題のインデックス（0 からスタート）
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default = True)

    objects = models.Manager()
    custom_objects = QuizSessionManager()

    def __str__(self):
        return f"{self.user} - {self.quiz} ({self.started_at})"
    
    def next_or_finish_question(self):
        next_index = self.current_index + 1
        total = len(self.question_order)
        if next_index >= total:
            self.finished_at = timezone.now()
            self.save(update_fields = [
                'finished_at'
            ])
        else:
            self.current_index+=1
            self.save(update_fields = ['current_index'])

    def check_session_finished(self):
        if self.finished_at and self.is_active is True:
            return True
        else:
            return False

    def is_active_false(self):
        self.is_active = False
        self.save(update_fields = ['is_active'])
    
    class Meta:
        #NOTE:1ユーザー、1クイズセッションのため。
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'quiz'],
                name = 'unique_user_quiz'
            )
        ]


class Answer(models.Model):
    session = models.ForeignKey('QuizSession', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('quizzes.Question', on_delete=models.CASCADE)
    choices = models.ManyToManyField('quizzes.Choice')# 複数選択肢に対応
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    custom_objects = AnswerManager()

    def __str__(self):
        return f"{self.session} - {self.question}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['session', 'question'],
                name = 'unique_session_question'
            )
        ]


