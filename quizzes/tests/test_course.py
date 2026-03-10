from .base import BaseTest
from django.urls import reverse
from quizzes.models import Course

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
                kwargs = {'course_uuid': course.uuid},
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
                kwargs = {'course_uuid': course.uuid},
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

