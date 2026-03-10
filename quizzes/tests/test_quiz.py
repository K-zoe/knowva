from .base import BaseTest
from django.urls import reverse
from quizzes.models import Quiz

class QuizCreateTest(BaseTest):
    def test_quiz_create_success(self):
        course = self.course_create()
        before = Quiz.objects.count()
        response = self.client.post(
            reverse(
                'quiz_create',
                kwargs = {'course_uuid': course.uuid}
            ),
            {
                'title': 'テストクイズ',
                'description': 'テストクイズの説明',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 302)
        after = Quiz.objects.count()
        self.assertNotEqual(before, after)

    def test_quiz_create_failure(self):
        course = self.course_create()
        before = Quiz.objects.count()
        response = self.client.post(
            reverse(
                'quiz_create',
                kwargs = {'course_uuid': course.uuid}
            ),
            {
                'title': '',
                'description': 'テストクイズの説明失敗',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 200)
        after = Quiz.objects.count()
        self.assertEqual(before, after)

class QuizEditTest(BaseTest):
    def test_quiz_edit_success(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        before = Quiz.objects.get(pk = quiz.pk)
        response = self.client.post(
            reverse(
                'quiz_edit',
                kwargs = {'course_uuid': course.uuid, 'quiz_uuid': quiz.uuid}
            ),
            {
                'title': 'テストクイズ編集',
                'description': 'テストクイズの説明編集',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 302)
        after = Quiz.objects.get(pk = quiz.pk)
        self.assertNotEqual(before.title, after.title)

    def test_quiz_edit_failure(self):
        course = self.course_create()
        quiz = self.quiz_create(course)
        before = Quiz.objects.get(pk = quiz.pk)
        response = self.client.post(
            reverse(
                'quiz_edit',
                kwargs = {'course_uuid': course.uuid, 'quiz_uuid': quiz.uuid}
            ),
            {
                'title': '',
                'description': 'テストクイズの説明編集失敗',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 200)
        after = Quiz.objects.get(pk = quiz.pk)
        self.assertEqual(before.title, after.title)
