from django.db import models

# Create your models here.
class WeekLikeRanking(models.Model):
    course = models.ForeignKey('quizzes.Course', on_delete=models.CASCADE, related_name='course_likeranking')
    period_start = models.DateField()
    like_count = models.PositiveIntegerField(default = 0)
    update_at = models.DateTimeField(auto_now=True)