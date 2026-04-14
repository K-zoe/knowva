from django.test import TestCase
from accounts.models import User

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