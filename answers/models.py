from django.db import models
from django.db.models import JSONField

class QuizSession(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE, related_name='sessions')

    # ランダム出題順を保存（SQLite なので JSONField）
    question_order = JSONField(null=True, blank=True)

    # 現在の問題のインデックス（0 からスタート）
    current_index = models.IntegerField(default=0)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.user} - {self.quiz} ({self.started_at})"
    
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

    # 複数選択肢に対応
    choices = models.ManyToManyField('quizzes.Choice')

    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session} - {self.question}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['session', 'question'],
                name = 'unique_session_question'
            )
        ]


