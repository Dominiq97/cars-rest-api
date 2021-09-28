from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_car( make='VW', model='Polo'):
    return models.CarManager.create_car(make, model)

class ModelTests(TestCase):

    def test_rate_str(self):
        rate = models.Rate.objects.create(
            rating=3,
            car_id=sample_car(),
        )

        self.assertEqual(str(rate), str(rate.rating))
