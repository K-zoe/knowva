from django.contrib import admin
from .models import WeekLikeRanking

@admin.register(WeekLikeRanking)
class RankingAdmin(admin.ModelAdmin):
    pass