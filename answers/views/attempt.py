from django.shortcuts import render,redirect
from django.http import Http404
from django.views.generic import View
from answers.forms import AnswerForm
from answers.service.quiz_service import QuizSessionService
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class AnswerAttemptView(LoginRequiredMixin, View):
    template_name = 'answers/answer.html'

    def dispatch(self, request, *args, **kwargs):
        self.course_uuid = kwargs.get('course_uuid')
        self.quiz_uuid = kwargs.get('quiz_uuid')
        #self.quiz = self.get_quiz(self.course_uuid, self.quiz_uuid)
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_service = QuizSessionService(
            self.course_uuid,
            self.quiz_uuid,
            self.user
        )
        
        #sessionの状態に合わせて、取得、作成、再作成。
        session = session_service.get_or_create_session()
        if session is None:
            raise Http404()
        
        question = session_service.get_question(session)
        if question is None:
            raise Http404()
        
        form = AnswerForm(question = question)
        context = {'question': question, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        session_service = QuizSessionService(self.user, self.quiz)

        session = session_service.get_session()
        if session is None:
            raise Http404()
        
        question = session_service.get_question(session)

        form = AnswerForm(request.POST, question = question)
        if not form.is_valid():
            return render(request, self.template_name, {'question': question, 'form': form})
        
        user_choice = form.cleaned_data['choices']

        answer = session_service.check_answer(session, user_choice)
        if answer is None:
            #TODO: エラー処理をどうするか。
            raise Http404()

        url_index = session.current_index
        session_service.next_or_finish_question(session)

        return redirect('answer_feedback', self.course_uuid, self.quiz_uuid, url_index)