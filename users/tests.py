from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='pass1234',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('pass1234'))
