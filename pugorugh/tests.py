from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import (
    APIRequestFactory, APITestCase, force_authenticate
    )

from . import models
from . import serializers
from . import views


# Create your tests here.


# model tests
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
        self.assertEqual(test_dog.status, 'u')


class UserPrefTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

        models.UserPref.objects.create(
            user=self.user,
            age='b, a, s',
            gender='m, f',
            size='s, m, l'
            )

    def test_user_pref(self):
        my_pref = models.UserPref.objects.get(user=self.user)

        self.assertEquals(my_pref.user.username, 'testuser')
        self.assertEqual(my_pref.age, 'b, a, s')

        self.assertRaises(AttributeError, setattr(
            my_pref, 'gender', ['m', 'f', 'u', 'm', 'm']))


#serializer test
class DogSerializerTestCASE(TestCase):

    def setUp(self):
        self.dog_attr = {
            'name': 'doug',
            'image_filename': '10.jpg',
            'breed': 'Chutney',
            'age': 3,
            'gender': 'f',
            'size': 'xl'
            }

        self.serializer_data = {
            'name': 'Emi',
            'image_filename': '11.jpg',
            'breed': 'BowWow',
            'age': 7,
            'gender': 'm',
            'size': 's'
            }
        self.dog = models.Dog.objects.create(**self.dog_attr)
        self.serializer = serializers.DogSerializer(instance=self.dog)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ['name', 'image_filename', 'breed',
                                            'age', 'gender', 'size', 'id'])

    def test_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['name'], self.dog_attr['name'])

    def test_gender_must_be_in_choices(self):
        self.dog_attr['gender'] = 's'
        serializer = serializers.DogSerializer(instance=self.dog,
                                               data=self.dog_attr)

        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ['gender'])


class UserPrefTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

        self.user_pref = {
            'user':self.user,
            'age':'y, a, s',
            'gender':'m, f',
            'size':'xl, m'
            }

        self.serializer_data = {
            'user':self.user,
            'age':'b, a, s',
            'gender':'m',
            'size':'xl, s'
            }
        self.preference = models.UserPref.objects.create(**self.user_pref)
        self.serializer = serializers.UserPrefSerializer(
            instance=self.preference)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ['id', 'age', 'gender', 'size'])

    def test_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['age'], self.user_pref['age'])

    def test_gender_must_be_in_choices(self):
        self.user_pref['gender'] = {'m', ' b', 'f'}
        serializer = serializers.UserPrefSerializer(
            instance=self.preference, data=self.user_pref)

        self.assertFalse(serializer.is_valid())


#view tests
class TestCreateUpdatePreference(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )
        self.user_pref = {
            'user': self.user,
            'age': 'y, a, s',
            'gender': 'm, f',
            'size': 'xl, m'
            }
        self.preference = models.UserPref.objects.create(**self.user_pref)

    def test_get(self):
        request = self.factory.get('/api/user/preferences/')
        force_authenticate(request, user=self.user)
        response = views.CreateUpdatePreference.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
                'id': 1,
                'age': 'y, a, s',
                'gender': 'm, f',
                'size': 'xl, m'
                })

    def test_put(self):
        request = self.factory.put(
            'api/user/preferences/',
            {
                'age': 'b, y, s',
                'gender': 'm',
                'size': 'xl, m'
                }, format='json'
            )
        force_authenticate(request, user=self.user)
        response = views.CreateUpdatePreference.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
                'id': 1,
                'age': 'b, y, s',
                'gender': 'm',
                'size': 'xl, m'
                })


class TestDogs(APITestCase):
    fixtures = ['dogs.json']

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

        self.user_pref = {
            'user': self.user,
            'age': 'y, a, s',
            'gender': 'm, f',
            'size': 'xl, m'
            }
        self.preference = models.UserPref.objects.create(**self.user_pref)

    def test_get(self):

        request = self.factory.get('api/dog/<pk>/undecided/next/')
        force_authenticate(request, user=self.user)
        response = views.Dogs.as_view()(request)

        self.assertEqual(response.status_code, 200)
