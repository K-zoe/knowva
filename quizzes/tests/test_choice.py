from .base import BaseTest
from django.urls import reverse
from quizzes.models import Question, Choice

class ChoiceCreateTest(BaseTest):
    def test_choice_create_success(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        before_question = Question.objects.count()
        before_choice = Choice.objects.count()
        response = self.client.post(
            reverse(
                'question_create',
                kwargs = {'quiz_uuid': quiz.uuid}
            ),
            {
                'title': 'テストクエッション',
                'text': 'テストクエッションの内容',
                'explanation': 'テストクエッションの解説',
                #管理フォーム
                'choice-TOTAL_FORMS': '2',
                'choice-INITIAL_FORMS': '0',
                'choice-MIN_NUM_FORMS': '0',
                'choice-MAX_NUM_FORMS': '1000',
                #データ1
                'choice-0-text': 'テストチョイス1',
                'choice-0-explanation': 'テストチョイス1の解説',
                'choice-0-is_correct': 'on',
                #データ2
                'choice-1-text': 'テストチョイス2',
                'choice-1-explanation': 'テストチョイス2の解説',
                'choice-1-is_correct': '',
            }
        )

        self.assertEqual(response.status_code, 302)
        after_question = Question.objects.count()
        after_choice = Choice.objects.count()
        self.assertNotEqual(before_question, after_question)
        self.assertNotEqual(before_choice, after_choice)

    def test_choice_create_failure(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        before_question = Question.objects.count()
        before_choice = Choice.objects.count()
        response = self.client.post(
            reverse(
                'question_create',
                kwargs = {'quiz_uuid': quiz.uuid}
            ),
            {
                'title': 'テストクエッション',
                'text': 'テストクエッションの内容',
                'explanation': 'テストクエッションの解説',
                #管理フォーム
                'choice-TOTAL_FORMS': '2',
                'choice-INITIAL_FORMS': '0',
                'choice-MIN_NUM_FORMS': '0',
                'choice-MAX_NUM_FORMS': '1000',
                #データ1
                'choice-0-text': 'テストチョイス1',
                'choice-0-explanation': 'テストチョイス1の解説',
                'choice-0-is_correct': 'on',
                #データ2
                'choice-1-text': '',
                'choice-1-explanation': 'テストチョイス2の解説',
                'choice-1-is_correct': '',
            }
        )

        self.assertEqual(response.status_code, 200)
        after_question = Question.objects.count()
        after_choice = Choice.objects.count()
        self.assertEqual(before_question, after_question)
        self.assertEqual(before_choice, after_choice)
        
class ChoiceEditTest(BaseTest):
    def test_choice_edit_success(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        question = self.question_create(quiz)
        choice1 = self.choice1_create(question)
        choice2 = self.choice2_create(question)

        response = self.client.post(
            reverse(
                'question_edit',
                kwargs = {
                    'course_uuid': course.uuid,
                    'quiz_uuid': quiz.uuid,
                    'question_uuid': question.uuid
                }
            ),
            {
                'title': 'テストクエッション編集',
                'text': 'テストクエッションの内容編集',
                'explanation': 'テストクエッションの解説編集',
                #管理フォーム
                'choice-TOTAL_FORMS': '2',
                'choice-INITIAL_FORMS': '1',
                'choice-MIN_NUM_FORMS': '0',
                'choice-MAX_NUM_FORMS': '1000',
                #データ1
                'choice-0-id': choice1.pk,
                'choice-0-text': 'テストチョイス1編集',
                'choice-0-explanation': 'テストチョイス1の解説編集',
                'choice-0-is_correct': 'on',
                #データ2
                'choice-1-id': choice2.pk,
                'choice-1-text': 'テストチョイス2',
                'choice-1-explanation': 'テストチョイス2の解説',
                'choice-1-is_correct': '',
            }
        )

        self.assertEqual(response.status_code, 302)
        after_choice1 = Choice.objects.get(pk = choice1.pk)
        self.assertNotEqual(choice1.text, after_choice1.text)
        after_choice2 = Choice.objects.get(pk = choice2.pk)
        self.assertEqual(choice2.text, after_choice2.text)

    def test_choice_edit_failure(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        question = self.question_create(quiz)
        choice1 = self.choice1_create(question)
        choice2 = self.choice2_create(question)

        response = self.client.post(
            reverse(
                'question_edit',
                kwargs = {
                    'course_uuid': course.uuid,
                    'quiz_uuid': quiz.uuid,
                    'question_uuid': question.uuid
                }
            ),
            {
                'title': 'テストクエッション編集',
                'text': 'テストクエッションの内容編集',
                'explanation': 'テストクエッションの解説編集',
                #管理フォーム
                'choice-TOTAL_FORMS': '2',
                'choice-INITIAL_FORMS': '1',
                'choice-MIN_NUM_FORMS': '0',
                'choice-MAX_NUM_FORMS': '1000',
                #データ1
                'choice-0-id': choice1.pk,
                'choice-0-text': '',
                'choice-0-explanation': 'テストチョイス1の解説編集',
                'choice-0-is_correct': 'on',
                #データ2
                'choice-1-id': choice2.pk,
                'choice-1-text': 'テストチョイス2',
                'choice-1-explanation': 'テストチョイス2の解説',
                'choice-1-is_correct': '',
            }
        )

        self.assertEqual(response.status_code, 200)
        after_choice1 = Choice.objects.get(pk = choice1.pk)
        self.assertEqual(choice1.text, after_choice1.text)
        after_choice2 = Choice.objects.get(pk = choice2.pk)
        self.assertEqual(choice2.text, after_choice2.text)