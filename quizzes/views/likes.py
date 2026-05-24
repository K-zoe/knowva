from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from quizzes.models import Course, Like

class LikeView(LoginRequiredMixin, View):
    template_name = 'quizzes/course_like_button.html'
    
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, uuid = kwargs.get('course_uuid'), is_public = True)
        return render(request, self.template_name, {'course': course})

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, uuid = kwargs.get('course_uuid'), is_public = True)
        like, created = Like.objects.get_or_create(
            user = self.request.user,
            course = course
        )
        if not created:
            like.delete()
            course.like_count -= 1
            course.save()
        else:
            course.like_count += 1
            course.save()
        return render(request, self.template_name, {'course': course})