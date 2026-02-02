from django.contrib import admin
from .models import User,Profile

@admin.register(User, Profile)
class UserAdmin(admin.ModelAdmin):
    pass