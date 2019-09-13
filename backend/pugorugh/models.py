from django.contrib.auth.models import User
from django.db import models

from multiselectfield import MultiSelectField


class Dog(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    UNKNOWN = 'u'
    SMALL = 's'
    MEDIUM = 'm'
    LARGE = 'l'
    XLARGE = 'xl'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown')
        ]

    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (XLARGE, 'Extra Large'),
        (UNKNOWN, 'Unknown')
        ]
    name = models.CharField(max_length=50)
    image_filename = models.ImageField(upload_to='static/images/dogs')
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=UNKNOWN
                              )
    size = models.CharField(
        max_length=1,
        choices=SIZE_CHOICES,
        default=UNKNOWN
        )


class UserDog(models.Model):
    LIKED = 'l'
    DISLIKED = 'd'
    DOG_STATUS = [
        (LIKED, 'Liked'),
        (DISLIKED, 'Disliked')
        ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    dog = models.ForeignKey(
        'Dog',
        on_delete=models.CASCADE
        )
    status = models.CharField(
        max_length=1,
        choices=DOG_STATUS,
        default=LIKED
        )


class UserPref(models.Model):
    BABY = 'b'
    YOUNG = 'y'
    ADULT = 'a'
    SENIOR = 's'
    MALE = 'm'
    FEMALE = 'f'
    UNKNOWN = 'u'
    SMALL = 's'
    MEDIUM = 'm'
    LARGE = 'l'
    XLARGE = 'xl'

    AGE_CHOICES = (
        (BABY, 'Baby'),
        (YOUNG, 'Young'),
        (ADULT, 'Adult'),
        (SENIOR, 'Senior')
    )

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown')
    )

    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (XLARGE, 'Extra Large'),
        (UNKNOWN, 'Unknown')

    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    age = MultiSelectField(
        choices=AGE_CHOICES,
        max_choices=4,
        )
    gender = MultiSelectField(
        choices=GENDER_CHOICES,
        max_choices=4
        )
    size = MultiSelectField(
        choices=SIZE_CHOICES,
        max_choices=4
        )
