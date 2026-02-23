from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from .models import (
    Course,
    Quiz,
    Question,
    Choice
)

class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'login_user',
            email = 'login_user@co.jp',
            password = 'test12345'
        )
        self.client.login(
            username = 'login_user@co.jp',
            password = 'test12345'
        )

    def course_create(self):
        course = Course.objects.create(
            title = 'テストコース',
            tag = 'テストタグ',
            user = self.user,
            description = 'テストコースの説明',
        )
        return course
    
    def quiz_create(self, course):
        course = self.course_create()
        quiz = Quiz.objects.create(
            course = course,
            title = 'テストクイズ',
        )
        return quiz

class CourseCreateTest(BaseTest):
    def test_course_create_success(self):
        before = Course.objects.count()
        response = self.client.post(
            reverse('course_create'),
            {
                'title': 'テストコース',
                'tag': 'テストタグ',
                'description': 'テストコースの説明',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 302)
        after = Course.objects.count()
        self.assertNotEqual(before, after)

    def test_course_create_failure(self):
        before = Course.objects.count()
        response = self.client.post(
            reverse('course_create'),
            {
                'title': "",
                'tag': "",
                'description': 'テストコース失敗',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 200)
        after = Course.objects.count()
        self.assertEqual(before, after)

class CourseEditTest(BaseTest):
    def test_course_edit_success(self):
        course = self.course_create()
        before = Course.objects.get(pk = course.pk)
        response = self.client.post(
            reverse(
                'course_edit',
                kwargs = {'course_pk': course.pk},
            ),
            {
                'title': 'テストコース編集',
                'tag': 'テストタグ編集',
                'description': 'テストコースの説明編集',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 302)
        after = Course.objects.get(pk = course.pk)
        self.assertNotEqual(before.title, after.title)

    def test_course_edit_failure(self):
        course = self.course_create()
        before = Course.objects.get(pk = course.pk)
        response = self.client.post(
            reverse(
                'course_edit',
                kwargs = {'course_pk': course.pk},
            ),
            {
                'title': "",
                'tag': "",
                'description': 'テストコースの説明編集失敗',
                'is_public': True
            }
        )

        self.assertEqual(response.status_code, 200)
        after = Course.objects.get(pk = course.pk)
        self.assertEqual(before.title, after.title)


class QuizCreateTest(BaseTest):
    pass

class QuizEditTest(BaseTest):
    pass

class QuestionCreateTest(BaseTest):
    pass

class QuestionEditTest(BaseTest):
    pass