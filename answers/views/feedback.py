from django.shortcuts import render
from django.http import Http404
from answers.service.session import SessionService
from answers.service.answer import AnswerService
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class FeedbackView(LoginRequiredMixin, View):
    template_name = 'answers/feedback.html'

    def dispatch(self,request, *args, **kwargs):
        self.course_uuid = kwargs.get('course_uuid')
        self.quiz_uuid = kwargs.get('quiz_uuid')
        self.user = request.user
        self.session_service = SessionService(
            self.course_uuid,
            self.quiz_uuid,
            self.user
        )
        return super().dispatch(request, *args, **kwargs)    

    def get(self, request, *args, **kwargs):
        session = self.session_service.get_session()
        
        #URLパラメーターのindexチェック
        current_index = session.current_index
        url_index = kwargs.get('index')
        if url_index is None:
            raise Http404('問題が見つかりません。')
        if url_index < 0 or url_index > current_index:
            raise Http404('問題が見つかりません。')
        
        answer_service = AnswerService(session)
        prev_index = answer_service.get_prev_index(url_index)
        next_index = answer_service.get_next_index(url_index, current_index)
        
        context = answer_service.get_feedback_data(url_index)
        context['session'] = session
        context['prev_index'] = prev_index
        context['next_index'] = next_index
        
        return render(request, self.template_name, context)