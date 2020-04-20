from itertools import chain

from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    """
    a class that defines the database representation of a Dog obj.

    subclasses django.db.models

    Attr:
        BABY: str()
            value if dog age is baby
        YOUNG: str()
            value if dog age is young
        ADULT: str()
            value if dog age is adult
        SENIOR:str()
            value if dog age is senior
        MALE : str()
            value if dog gender is male
        FEMALE: str()
            value if dog gender is female
        UNKNOWN: str()
            value if gender is not known
        SMALL: str()
            value if dog size is small
        MEDIUM: str()
            value if dog size is medium
        LARGE: str()
            value if dog size is large
        X_LARGE: str()
            value if dog size is X Large

        GENDER_CHOICES: list()
            list of two tuples defining available
            attribute values for Dog objects gender

        SIZE_CHOICES: list()
            list of two tuples defining available
            attribute values for Dog objects size

        name: django ORM CharField obj()
            defines database column for Dogs name

        image_filename: django ORM CharField obj()
            defines database column for Dogs image_filename

        breed:  django ORM CharField obj()
            defines database column for Dog breed

        age: django ORM IntegerField obj()
            defines database column for Dog age

        gender: django ORM CharField obj()
            defines database column for Dog gender
            :argument GENDER_CHOICES

        size:  django ORM CharField obj()
            defines database column for Dog size
            :argument SIZE_CHOICES
    """
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
    X_LARGE = 'xl'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown')
        ]

    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (X_LARGE, 'Extra Large'),
        (UNKNOWN, 'Unknown')
        ]

    name = models.CharField(max_length=50, blank=True, default='')
    image_filename = models.CharField(max_length=100, blank=True, default='')
    breed = models.CharField(max_length=50, default='')
    age = models.IntegerField()
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=UNKNOWN
        )
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        default=UNKNOWN
        )


class UserDog(models.Model):
    """
    a class that defines the database representation of a UserDog obj

    subclasses django.db.models

    Attr:
        LIKED: str()
            value if UserDog status is liked
        DISLIKED: str()
            value if UserDog status is disliked
        UNDECIDED: str()
            value if UserDog status is undecided

        DOG_STATUS: list()
            list of two tuples defining available
            attribute values for UserDog attr status

        user: django ORM ForeignKeyField obj()
            defines database one to many relation to User
        dog: django ORM ForeignKeyField obj()
            defines database one to many relation to Model.Dog
        status:  django ORM CharField obj()
            defines database column for UserDog status
            :argument DOG_STATUS
    """
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
    """
    a class that defines the database representation of a UserPref obj.

    subclasses django.db.models

    Attr:
        BABY: str()
            value if dog age is baby
        YOUNG: str()
            value if dog age is young
        ADULT: str()
            value if dog age is adult
        SENIOR:str()
            value if dog age is senior
        MALE : str()
            value if dog gender is male
        FEMALE: str()
            value if dog gender is female
        UNKNOWN: str()
            value if gender is not known
        SMALL: str()
            value if dog size is small
        MEDIUM: str()
            value if dog size is medium
        LARGE: str()
            value if dog size is large
        X_LARGE: str()
            value if dog size is X Large

        GENDER_CHOICES: list()
            list of two tuples defining available
            attribute values for Dog objects gender

        SIZE_CHOICES: list()
            list of two tuples defining available
            attribute values for Dog objects size

        AGE_CHOICES: list()
            list of two tuples defining available
            attribute values for Dog objects size

        user: django ORM ForeignKeyField obj()
            defines database one to many relation to User

        age: django ORM CharField obj()
            defines database column for UserPref age
            :argument AGE_CHOICES

        gender: django ORM CharField obj()
            defines database column for UserPref gender
            :argument GENDER_CHOICES

        size:  django ORM CharField obj()
            defines database column for UserPref size
            :argument SIZE_CHOICES

    Method:
        get_age_display
    """
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
    X_LARGE = 'xl'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown')
        ]

    SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (X_LARGE, 'Extra Large'),
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
        """
        converts sequence of UserPref.age values to a frozenset of chained range

        :rtype: frozenset
        """
        ls = []
        age = self.age.split(',')
        if len(age) > 0:
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
