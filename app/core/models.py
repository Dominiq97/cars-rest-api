from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.deletion import CASCADE

class CarManager():
    def create_car(make, model):
        if not make:
            raise ValueError('A car should have an make')
        if not model:
            raise ValueError('A car should have an model')
        car = Car(make=make,model=model)
        car.save()
        return car

class Car(models.Model):
    make =  models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    avg_rating = models.FloatField(default=0)
    rates_number = models.IntegerField(default=0)
    def __str__(self):
        return self.make

    

class Rate(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating)

    

