from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user(self):
        email = 'catanadominic@gmail.com'
        password = 'Password'
        user = get_user_model().objects.create_user(email=email,
                        password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_sensitive_case_mail(self):
        email = 'catanadominic@GMAIL.com'
        user = get_user_model().objects.create_user(email, 'tests')

        self.assertEqual(user.email, email.lower())

    def test_invalid_mail(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'tests')

    def test_superuser(self):
        user = get_user_model().objects.create_superuser('catanadominic@gmail.com', 
        'test')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
