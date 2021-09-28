from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.deletion import CASCADE

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('A user should have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CarManager():
    def create_car(make, model):
        if not make:
            raise ValueError('A car should have an make')
        if not model:
            raise ValueError('A car should have an model')
        car = Car(make=make,model=model)
        car.save()
        return car

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

class Car(models.Model):
    make =  models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    avg_rating = models.FloatField(default=0)
    def __str__(self):
        return self.make

    

class Rate(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating)

    

