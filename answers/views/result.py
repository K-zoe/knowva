from django.shortcuts import render
from django.http import Http404
from django.views.generic import View
from answers.service.quiz_service import QuizSessionService
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class QuizResultView(LoginRequiredMixin, View):
    #NOTE: 全体の結果表示
    template_name = 'answers/result.html'

    def dispatch(self, request, *args, **kwargs):
        self.course_uuid = kwargs.get('course_uuid')
        self.quiz_uuid = kwargs.get('quiz_uuid')
        self.quiz = self.get_quiz(self.course_uuid, self.quiz_uuid)
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_service = QuizSessionService(self.user, self.quiz)
        session = session_service.get_session()
        if session is None:
            raise Http404()
        
        if session_service.check_session_finished(session) is False:
            raise Http404()
        
        score = session_service.calculate_score(session)
        context = {
            'session': session,
            'score': score
        }
        return render(request, self.template_name, context)