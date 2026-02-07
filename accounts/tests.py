from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class  SignupTest(TestCase):

    def test_signup_success(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username':'testuser',
                'email':'test@co.jp',
                'password1':'test12345',
                'password2':'test12345'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username = 'testuser').exists())
        self.assertIn('_auth_user_id', self.client.session)

    def test_signup_failure(self):
        #NOTE: すでに登録済みのユーザーで登録ができないことをチェック。別パターンのテストを用意してもいいかも
        User.objects.create_user(
            username = 'fail_user',
            email = 'fail_user@co.jp',
            password = 'test12345'
        )

        response = self.client.post(
            reverse('signup'),
            {
                'username':'fail_user',
                'email':'fail_user@co.jp',
                'password1':'test12345',
                'password2':'test12345'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

class LoginTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username = 'login_user',
            email = 'login_user@co.jp',
            password = 'test12345'
        )

    def test_login_success(self):
        response = self.client.post(
            reverse('login'),
            {
                'username':'login_user@co.jp',
                'password':'test12345'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_failure(self):
        response = self.client.post(
            reverse('login'),
            {
                'username':'login_fail',
                'password':'login_fail12345'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)



