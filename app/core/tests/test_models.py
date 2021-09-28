from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_car( make='VW', model='Polo'):
    return models.CarManager.create_car(make, model)

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

    def test_rate_str(self):
        rate = models.Rate.objects.create(
            rating=3,
            car_id=sample_car(),
        )

        self.assertEqual(str(rate), str(rate.rating))
