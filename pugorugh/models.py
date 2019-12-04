from django.contrib.auth.models import User
from django.db import models

from multiselectfield import MultiSelectField

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

AGE_CHOICES = [
        (BABY, 'Baby'),
        (YOUNG, 'Young'),
        (ADULT, 'Adult'),
        (SENIOR, 'Senior')
    ]


class Dog(models.Model):

    name = models.CharField(max_length=50,blank=True, default='')
    image_filename = models.CharField(max_length=100, blank=True, default='')
    breed = models.CharField(max_length=50, default='')
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
    UNDECIDED = 'u'

    DOG_STATUS = [
        (LIKED, 'Liked'),
        (DISLIKED, 'Disliked'),
        (UNDECIDED, 'Undecided')
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
        default=UNDECIDED
        )


class UserPref(models.Model):

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
        max_choices=2
        )

    size = MultiSelectField(
        choices=SIZE_CHOICES,
        max_choices=4
        )
