from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from quizzes.models import (
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
        quiz = Quiz.objects.create(
            course = course,
            title = 'テストクイズ',
        )
        return quiz
    
    def question_create(self, quiz):
        question = Question.objects.create(
            quiz = quiz,
            title = 'テスト質問',
            text = 'テスト質問の内容',
            explanation = 'テスト質問の解説'
        )

        return question

    def choice1_create(self, question):
        choice1 = Choice.objects.create(
            question = question,
            text = 'テストチョイス',
            explanation = 'テストチョイスの解説',
            is_correct = True
        )

        return choice1
    
    def choice2_create(self, question):
        choice2 = Choice.objects.create(
            question = question,
            text = 'テストチョイス2',
            explanation = 'テストチョイス2の解説',
            is_correct = False
        )

        return choice2