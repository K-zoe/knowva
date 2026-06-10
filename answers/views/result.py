from django.shortcuts import render
from django.http import Http404
from answers.service.session import SessionService
from answers.service.result import ResultService
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class ResultView(LoginRequiredMixin, View):
    #NOTE: 全体の結果表示
    template_name = 'answers/result.html'

    def dispatch(self, request, *args, **kwargs):
        self.course_uuid = kwargs.get('course_uuid')
        self.quiz_uuid = kwargs.get('quiz_uuid')
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_service = SessionService(self.course_uuid, self.quiz_uuid, self.user)
        session = session_service.get_session()
        if not session_service.check_session_finished(session):
            raise Http404()
        
        result_serivice = ResultService(session)
        score = result_serivice.calculate_score()
        context = {
            'session': session,
            'score': score
        }
        return render(request, self.template_name, context)