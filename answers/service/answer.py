from quizzes.models import Question, Choice
from answers.models import Answer
from django.db import IntegrityError

class AnswerService:
    def __init__(self, session):
        self.session = session

    def get_prev_index(self, url_index) -> int | None:
        if url_index == 0:
            return None
        
        elif url_index > 0:
            return url_index -1

    def get_next_index(self, url_index, current_index) -> int | None:
        #url_indexが現在のindexで、かつsessionが終了している場合はNone
        if url_index == current_index and self.session.finished_at:
            return None
        #url_indexに1足したindexが現在のindexで、かつsessionが終了していない場合はNone
        elif url_index + 1 == current_index and self.session.finished_at is None:
            return None
        #url_indexが現在のindexより小さく。
        elif url_index < current_index and url_index >= 0:
            return url_index + 1
        
        else:
            return None
        
    def check_answer(self, user_choice) -> Answer | None:
        #NOTE: 回答の正誤を判定して保存する。
        question_pk = self.session.question_order[self.session.current_index]
        question = Question.objects.filter(pk = question_pk).first()
        choices = Choice.objects.filter(
            question = question,
            is_correct = True
        ).values_list('pk', flat = True)

        if set(map(int, user_choice)) == set(choices):
            is_correct = True
        else:
            is_correct = False

        try:
            answer = Answer.objects.create(
                session = self.session,
                question = question,
                is_correct = is_correct
            )
            answer.choices.add(*user_choice)
            return answer
        
        except IntegrityError:
            return None
        
    def get_feedback_data(self, url_index):
        question_pk = self.session.question_order[url_index]
        answer = Answer.objects.for_feedback().by_session_and_question(
            self.session,
            question_pk
        )
        question = answer.question
        choices = question.choice.all()
        selected_choices = answer.choices.all()

        return {
            'answer': answer,
            'question': question,
            'choices': choices,
            'selected_choices': selected_choices,
        }
        
    def get_answer_choice(self,question_pk):
        answers = Answer.objects.for_feedback(). by_session_and_question(
            self.session,
            question_pk,
        )
        answer_choice = answers.choice.all()
        if answer_choice is None:
            raise ValueError()
        return answer_choice