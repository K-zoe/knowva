from django.shortcuts import render,redirect
from django.http import Http404
from answers.forms import AnswerForm
from answers.service.session import SessionService
from answers.service.answer import AnswerService
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class AttemptView(LoginRequiredMixin, View):
    template_name = 'answers/attempt.html'

    def dispatch(self, request, *args, **kwargs):
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
        #sessionの状態に合わせて、取得、作成、再作成。
        session = self.session_service.get_or_create_session()
        question = self.session_service.get_question(session)
        
        form = AnswerForm(question = question)
        context = {'question': question, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        session = self.session_service.get_session()
        question = self.session_service.get_question(session)

        form = AnswerForm(request.POST, question = question)
        if not form.is_valid():
            return render(request, self.template_name, {'question': question, 'form': form})
        
        user_choice = form.cleaned_data['choices']
        answer_service = AnswerService(session)
        answer_service.check_answer(user_choice)

        url_index = session.current_index
        session.next_or_finish_question()

        return redirect('answer_feedback', self.course_uuid, self.quiz_uuid, url_index)