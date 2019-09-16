from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from . import models
# Create your tests here.


class DogTestCase(TestCase):
    def setUp(self):
        models.Dog.objects.create(
            name='George',
            image_filename='13.jpg',
            age=12,
            gender='m',
            size='xl',
            )

    def test_dog(self):
        dog = models.Dog.objects.get(name='George')
        self.assertIsInstance(dog, models.Dog)
        self.assertEqual(hasattr(dog, 'age'), True)
        self.assertEqual(getattr(dog, 'gender'), 'm')
        self.assertEqual(dog.image_filename, '13.jpg')


class UserDogTestCAse(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

        models.Dog.objects.create(
            name='George',
            image_filename='13.jpg',
            age=12,
            gender='m',
            size='xl',
            )

    def test_userdog(self):
        test_dog = models.UserDog.objects.create(
           dog=models.Dog.objects.get(name='George'),
           user=self.user
           )
        self.assertEqual(test_dog.dog.id, 1)
        self.assertEqual(test_dog.user.username, 'testuser')
        self.assertIsInstance(test_dog.dog, models.Dog)
        self.assertEqual(test_dog.status, 'l')


class UserPrefTest(TestCase):

    def setUp(self):

        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

        models.UserPref.objects.create(
            user=self.user,
            age=['b', 'a', 's'],
            gender=['m', 'f', 'u'],
            size=['s', 'm', 'xl', 'l'],
            )

    def test_user_pref(self):
        my_pref = models.UserPref.objects.get(user=self.user)

        self.assertEquals(my_pref.user.username, 'testuser')
        self.assertEqual(my_pref.age, ['b', 'a', 's'])

        self.assertRaises(AttributeError,  setattr(
            my_pref, 'gender', ['m', 'f', 'u', 'm', 'm']))
