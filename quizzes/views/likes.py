from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.db.models import F
from quizzes.models import Course, Like

class LikeView(LoginRequiredMixin, View):
    template_name = 'quizzes/course_like_button.html'

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, uuid = kwargs.get('course_uuid'), is_public = True)

        with transaction.atomic():
            like, created = Like.objects.get_or_create(
                user = self.request.user,
                course = course
            )
            if not created:
                like.delete()
                Course.objects.filter(pk = course.pk).update(like_count = F('like_count') - 1)
                liked = False
            else:
                Course.objects.filter(pk = course.pk).update(like_count = F('like_count') + 1)
                liked = True

        course.refresh_from_db(fields = ['like_count'])
        return render(request, self.template_name, {'course': course, 'liked': liked})