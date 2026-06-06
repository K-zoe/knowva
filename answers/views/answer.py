from django.shortcuts import render,get_object_or_404, redirect
from django.http import Http404
from django.views.generic import View
from quizzes.models import Question, Choice
from answers.models import Answer
from answers.forms import AnswerForm
from answers.service.quiz_service import QuizSessionService

class AnswerAttemptView(View):
    template_name = 'answers/answer.html'

    def dispatch(self, request, *args, **kwargs):
        self.course_uuid = kwargs.get('course_uuid')
        self.quiz_uuid = kwargs.get('quiz_uuid')
        self.quiz = self.get_quiz(self.course_uuid, self.quiz_uuid)
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_service = QuizSessionService(self.user, self.quiz)
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

class AnswerFeedbackView(BaseView, View):
    template_name = 'answers/answer_feedback.html'

    def dispatch(self,request, *args, **kwargs):
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
        
        #URLパラメーターのindexチェック
        current_index = session.current_index
        url_index = kwargs.get('index')
        if url_index is None:
            raise Http404()
        if url_index < 0 or url_index > current_index:
            raise Http404()
        
        #画面に表示させるURL制御
        prev_index = session_service.get_prev_index(url_index)
        next_index = session_service.get_next_index(session, url_index, current_index)

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
    
class QuizResultView(BaseView, View):
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