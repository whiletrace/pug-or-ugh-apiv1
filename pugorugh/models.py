from django.contrib.auth.models import User
from django.db import models
from itertools import chain

from multiselectfield import MultiSelectField


class Dog(models.Model):
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

    name = models.CharField(max_length=50, blank=True, default='')
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
        null=True,
        related_name='dogs_user',
        related_query_name='dogs_user_query',
        on_delete=models.CASCADE
        )

    dog = models.ForeignKey(
        'Dog',
        null=True,
        related_name='users_dog',
        related_query_name='user_dogs_query',

        on_delete=models.CASCADE
        )

    status = models.CharField(
        max_length=1,
        choices=DOG_STATUS,
        default=UNDECIDED
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

    user = models.ForeignKey(
        User,
        related_name='userpref',
        on_delete=models.CASCADE
        )

    age = models.CharField(
        choices=AGE_CHOICES,
        default='',
        blank=True,
        max_length=10
        )

    gender = models.CharField(
        choices=GENDER_CHOICES,
        default='',
        blank=True,
        max_length=4

        )

    size = models.CharField(
        choices=SIZE_CHOICES,
        default='',
        blank=True,
        max_length=10
        )

    def get_age_display(self):
        ls = []
        age = self.age.split(',')
        if len(age) > 1:
            for a in age:
                if a == 'b':
                    ls.append(range(1, 19))
                elif a == 'y':
                    ls.append(range(19, 37))
                elif a == 'a':
                    ls.append(range(37, 57))
                elif a == 's':
                    ls.append(range(57, 100))
        chained = frozenset(chain.from_iterable(ls))
        return chained







