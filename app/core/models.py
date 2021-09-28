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
    rates_number = models.IntegerField(default=0)

class Rate(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)

    

