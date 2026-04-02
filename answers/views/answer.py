from django.shortcuts import render,get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from answers.mixins.attempt import (
    QuizSessionMixin,
    QuizObjectMixin,
    AnswerCheckMixin
)
from quizzes.models import (
    Course,
    Quiz,
    Question,
    Choice
)
from answers.models import(
    QuizSession,
    Answer
)
from django.db import transaction

class AnswerAttempView(
    LoginRequiredMixin,
    QuizSessionMixin,
    QuizObjectMixin,
    AnswerCheckMixin,
    View
):
    template_name = 'answers/answer.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = self.get_quiz(kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session = self.check_and_get_session(self.quiz)
        question = self.get_question(session)
        if question is None:
            #NOTE: 
            return render()
        context = {'question': question}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        session = self.get_session(self.quiz)
        user_choice = request.POST.getlist('choice')
        #NOTE: session情報を前提にする。
        self.check_answer(session, user_choice)

        url_index = session.current_index

        self.next_or_finish_question(session)

        if session is None:
            pass
        #status = self.next_or_finish_question(session)
        return redirect('answer_feedback', kwargs.get('course_uuid'), kwargs.get('quiz_uuid'), url_index)

class AnswerFeedbackView(LoginRequiredMixin, QuizSessionMixin, QuizObjectMixin, View):
    template_name = 'answers/answer_feedback.html'

    def dispatch(self,request, *args, **kwargs):
        self.quiz = self.get_quiz(kwargs)
        return super().dispatch(request, *args, **kwargs)    

    def get_prev_index(self, session, url_index, current_index):
        if url_index == 0:
            return None
        
        elif url_index > 0:
            return url_index -1
        
    def get_next_index(self, session, url_index, current_index):

        if url_index == current_index and session.finished_at:
            return None
        
        elif url_index + 1 == current_index and session.finished_at is None:
            return None

        elif url_index < current_index and url_index >= 0:
            return url_index + 1
        
        else:
            return None

    def get(self, request, *args, **kwargs):
        session = self.get_session(self.quiz)
        current_index = session.current_index
        url_index = kwargs.get('index')

        if url_index is None:
            raise Http404()
        if url_index < 0 or url_index > current_index:
            raise Http404()
        
        #画面に表示させるURL制御
        prev_index = self.get_prev_index(session, url_index, current_index)
        next_index = self.get_next_index(session, url_index, current_index)

        question_pk = session.question_order[url_index]
        question = get_object_or_404(
            Question,
            pk = question_pk
        )
        

        choice = Choice.objects.filter(
            question = question
        ).all()

        answer = get_object_or_404(
            Answer,
            session = session,
            question = question
        )

        selected_choices = answer.choices.all()

        context = {
            'session':session,
            'answer':answer,
            'question':question,
            'choices':choice,
            'selected_choices':selected_choices,
            'prev_index':prev_index,
            'next_index':next_index
        }
        return render(request, self.template_name, context)