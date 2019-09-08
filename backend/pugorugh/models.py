from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=50)
    image_filename = models.ImageField(upload_to='static/images/dogs')
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    size = models.CharField(max_length=1)


class UserDog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    dog = models.ForeignKey(
        'Dog',
        on_delete=models.CASCADE
        )
    status = models.CharField(max_length=1)


class UserPref(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    age = models.CharField(max_length=1)
    gender = models.CharField(max_length=1)
    size = models.CharField(max_length=2)

