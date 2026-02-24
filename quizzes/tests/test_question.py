from .base import BaseTest
from django.urls import reverse
from quizzes.models import Question, Choice


class QuestionCreateTest(BaseTest):
    def test_question_create_success(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        before_question = Question.objects.count()
        before_choice = Choice.objects.count()
        response = self.client.post(
            reverse(
                'question_create',
                kwargs = {'quiz_pk': quiz.pk}
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

    def test_question_create_failure(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        before_question = Question.objects.count()
        before_choice = Choice.objects.count()
        response = self.client.post(
            reverse(
                'question_create',
                kwargs = {'quiz_pk': quiz.pk}
            ),
            {
                'title': '',
                'text': 'テストクエッションの内容失敗',
                'explanation': 'テストクエッションの解説失敗',
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

        self.assertEqual(response.status_code, 200)
        after_question = Question.objects.count()
        after_choice = Choice.objects.count()
        self.assertEqual(before_question, after_question)
        self.assertEqual(before_choice, after_choice)

class QuestionEditTest(BaseTest):
    def test_question_edit_success(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        question = self.question_create(quiz)
        before_question = Question.objects.get(pk = question.pk)
        response = self.client.post(
            reverse(
                'question_edit',
                kwargs = {
                    'course_pk': course.pk,
                    'quiz_pk': quiz.pk,
                    'question_pk': question.pk
                }
            ),
            {
                'title': 'テストクエッション編集',
                'text': 'テストクエッションの内容編集',
                'explanation': 'テストクエッションの解説編集',
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
        after_question = Question.objects.get(pk = question.pk)
        self.assertNotEqual(before_question.title, after_question.title)

    def test_question_edit_failure(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        question = self.question_create(quiz)
        before_question = Question.objects.get(pk = question.pk)
        response = self.client.post(
            reverse(
                'question_edit',
                kwargs = {
                    'course_pk': course.pk,
                    'quiz_pk': quiz.pk,
                    'question_pk': question.pk
                }
            ),
            {
                'title': '',
                'text': 'テストクエッションの内容編集失敗',
                'explanation': 'テストクエッションの解説編集失敗',
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

        self.assertEqual(response.status_code, 200)
        after_question = Question.objects.get(pk = question.pk)
        self.assertEqual(before_question.title, after_question.title)
