from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import (
    APIRequestFactory, APITestCase, force_authenticate
    )

from . import models
from . import serializers
from . import views


# model tests
class DogTestCase(TestCase):
    """
    class encapsulates setup and unittests for models.Dog

    subclasses django.test TestCase

    methods:
        setUp,
        test_dog

    """

    def setUp(self):
        """Creates a models.dog object in test database."""
        models.Dog.objects.create(
            name='George',
            image_filename='13.jpg',
            age=12,
            gender='m',
            size='xl',
            )

    def test_dog(self):
        """Unittest for models.Dog.

        asserts that an object is an instance of models.dog
        asserts that object attributes match attributes set by DogTestCase.setUp
        asserts that object attribute values match object created in
        DogTestCase.setUp
        """
        dog = models.Dog.objects.get(name='George')
        self.assertIsInstance(dog, models.Dog)
        self.assertEqual(hasattr(dog, 'age'), True)
        self.assertEqual(getattr(dog, 'gender'), 'm')
        self.assertEqual(dog.image_filename, '13.jpg')


class UserDogTestCAse(TestCase):
    """class encapsulates setup and unittests for models.UserDog

    subclasses django.test TestCase

    :methods
        setUp,
        test_userdog
    """

    def setUp(self):
        """
        Creates a User and models.dog object in test database.

        attribute:
            user:
                User obj with attributes of username, email, and password set
            dog:
                models.Dog obj with attributes of name, image_file,
                age, gender, and size
            test_dog:
                models. UserDog obj with attributes of dog, user
        """
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

        self.dog = models.Dog.objects.create(
            name='George',
            image_filename='13.jpg',
            age=12,
            gender='m',
            size='xl',
            )
        self.test_dog = models.UserDog.objects.create(
            dog=models.Dog.objects.get(name='George'),
            user=self.user
            )

    def test_userdog(self):
        """Unittest for models.UserDog.

        asserts that an object has expected id
        asserts that object attributes match
        attributes set by UserDogTestCase.setUp asserts that object attribute
        values match object created in UserDogTestCase.setUp
        """

        self.assertEqual(self.test_dog.dog.id, 1)
        self.assertEqual(self.test_dog.user.username, 'testuser')
        self.assertIsInstance(self.test_dog.dog, models.Dog)
        self.assertEqual(self.test_dog.status, 'u')


class UserPrefTest(TestCase):
    """class encapsulates setup and unittests for models.UserPref

    subclasses django.test TestCase

    :methods
        setUp,
        test_user_pref
    """

    def setUp(self):
        """
        Creates a User and models.UserPref object in test database

        attribute:
            user:
                User obj with attributes of username, email, and password set

            my_pref:
                instantiates a UserPref object in relation to user
        """
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

        self.my_pref = models.UserPref.objects.get(user=self.user)

    def test_user_pref(self):
        """Unittest for models.UserPref.

        asserts that object attribute
        values match object created in UserPrefTest.setUp
        """
        self.assertEquals(self.my_pref.user.username, 'testuser')
        self.assertEqual(self.my_pref.age, 'b, a, s')

        self.assertRaises(AttributeError, setattr(
            self.my_pref, 'gender', ['m', 'f', 'u', 'm', 'm']))


#serializer test
class DogSerializerTestCASE(TestCase):
    """class encapsulates setup and unittests for serializers.DogSerializer

    subclasses django.test TestCase

    :methods
        setUp, test_contains_expected_fields,
        test_field_content, test_gender_must_be_in_choices
    """

    def setUp(self):
        """
        Creates a User and models.UserPref object in test database

        attribute:
            dog_attr:
                dictionary that with key value pairs that would
                describe a models.dog object

            serializer_data:
                dictionary that describe with key value pairs that would
                describe a models.dog object

            dog:
                models.Dog object instantiated with dog_attr dictionary

            serializer
                serializers.DogSerializer object

        """
        self.dog_attr = {
            'name':'doug',
            'image_filename':'10.jpg',
            'breed':'Chutney',
            'age':3,
            'gender':'f',
            'size':'xl'
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
        """Unittest for serializers.DogSerializer.

        asserts that serializer object keys match expectations
        """
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ['name', 'image_filename', 'breed',
                                            'age', 'gender', 'size', 'id'])

    def test_field_content(self):
        """Unittest for serializers.DogSerializer.

        asserts that serializer attributes, match dictionary keys
        of dog_attr dictionary used to construct the object
        """
        data = self.serializer.data

        self.assertEqual(data['name'], self.dog_attr['name'])

    def test_gender_must_be_in_choices(self):
        """Unittest for serializers.DogSerializer.

        asserts that that if serializer receives a unexpected value
        an exception is thrown
        """
        self.dog_attr['gender'] = 's'
        serializer = serializers.DogSerializer(instance=self.dog,
                                               data=self.dog_attr)

        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ['gender'])


class UserPrefTestCase(TestCase):
    """class encapsulates setup and unittests for serializers.DogSerializer

    subclasses django.test TestCase

    :methods
        setUp, test_contains_expected_fields,
        test_field_content, test_gender_must_be_in_choices
    """

    def setUp(self):
        """
        Creates a User and models.UserPref object in test database

        attribute:
            dog_attr:
                dictionary that with key value pairs that would
                describe a models.dog object

            serializer_data:
                dictionary that describe with key value pairs that would
                describe a models.dog object

            dog:
                models.Dog object instantiated with dog_attr dictionary

            serializer
                serializers.DogSerializer object

        """
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
        """Unittest for serializers.UserPrefSerializer.

        asserts that serializer object keys match expectations
        """
        data = self.serializer.data

        self.assertCountEqual(data.keys(), ['id', 'age', 'gender', 'size'])

    def test_field_content(self):
        """Unittest for serializers.UserPrefSerializer.

        asserts that serializer attributes, match dictionary keys
        of user_pref dictionary used to construct the object
        """
        data = self.serializer.data

        self.assertEqual(data['age'], self.user_pref['age'])

    def test_gender_must_be_in_choices(self):
        """Unittest for serializers.DogSerializer.

        asserts that that if serializer receives a unexpected value
        an exception is thrown
        """
        self.user_pref['gender'] = {'m', ' b', 'f'}
        serializer = serializers.UserPrefSerializer(
            instance=self.preference, data=self.user_pref)

        self.assertFalse(serializer.is_valid())


#view tests
class TestCreateUpdatePreference(APITestCase):
    """class encapsulates setup and unittests for
    views.TestCreateUpdatePreference.

    subclasses rest_framework.test.APITestCase

    :methods
        setUp, test_get, test_put
    """

    def setUp(self):
        """Creates a User and models.UserPref object in test database

        attribute:
            factory:
                rest_framework.test.ApIRequestFactory object

            user:
                User object with username, email, and password set

            user_pref:
                dictionary that describe with key value pairs that would
                describe a models.UserPref object

            preference:
                models.UserPref object instantiated with dog_attr dictionary
        """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )
        self.user_pref = {
            'user':self.user,
            'age':'y, a, s',
            'gender':'m, f',
            'size': 'xl, m'
            }
        self.preference = models.UserPref.objects.create(**self.user_pref)

    def test_get(self):
        """Unittest tests retrieve and update operations of views.UpdateStatus

        Asserts that status code will be 200
        Asserts that the response data is as expected
        """
        request = self.factory.get('/api/user/preferences/')
        force_authenticate(request, user=self.user)
        response = views.CreateUpdatePreference.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id':1,
            'age':'y, a, s',
            'gender':'m, f',
            'size':'xl, m'
            })

    def test_put(self):
        """Unittest tests retrieve and update operations of views.UpdateStatus

        Asserts that status code will be 200
        Asserts that the response data is as expected
        """
        request = self.factory.put(
            'api/user/preferences/',
            {
                'age':'b, y, s',
                'gender':'m',
                'size':'xl, m'
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
    """Class encapsulates setup and unittests for views.Dogs.

    subclasses rest_framework.test.APITestCase

    attributes:
        fixtures
            json encoded data that is preloaded into test database

    methods:
        setUp, test_get
    """
    fixtures = ['dogs.json']

    def setUp(self):
        """Creates a User and models.UserPref object in test database

        attribute:
            factory:
                rest_framework.test.ApIRequestFactory object

            user:
                User object with username, email, and password set

            user_pref:
                dictionary with key value pairs that would
                describe a models.UserPref object

            preference:
                models.UserPref object instantiated with user_pref dictionary
        """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

        self.user_pref = {
            'user':self.user,
            'age':'y, a, s',
            'gender':'f',
            'size':'xl'
            }
        self.preference = models.UserPref.objects.create(**self.user_pref)

    def test_get(self):
        """Unittest tests retrieve and update operations of views.Dog

        Asserts that response status code will be 200
        """
        request = self.factory.get('api/dog/<pk>/<conv:status>/next/')
        force_authenticate(request, user=self.user)
        response = views.Dogs.as_view()(request, pk=-1, status='undecided')

        self.assertEqual(response.status_code, 200)


class TestUpdateStatus(APITestCase):
    """class encapsulates setup and unittests for views.TestUpdateStatus.

    subclasses rest_framework.test.APITestCase

    attribute:
        fixtures
            json encoded data that is preloaded into test database

    methods:
        setUp, test_put
    """
    fixtures = ['dogs.json']

    def setUp(self):
        """Creates a User and models.UserPref object in test database

        attribute:
            factory:
                rest_framework.test.ApIRequestFactory object

            user:
                User object with username, email, and password set
        """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='testuser',
            email='loser@loser.com',
            password='password'
            )

    def test_put(self):
        """Unittest tests update operations of views.UpdateStatus.

        asserts that response status code will be 200, asserts that related
        UserDog object status attributes value is 'l'

        """
        request = self.factory.put('api/dog/<pk>/<conv:status>/')
        force_authenticate(request, user=self.user)
        response = views.UpdateStatus.as_view()(request, pk=2, status='liked')
        self.assertEqual(response.status_code, 200)
        user_id = self.user.id
        queryset = models.Dog.objects.filter(user_dogs_query__user_id=user_id)
        dog = queryset.filter(pk=2).get().users_dog.select_related().filter(
            user=self.user).get()
        self.assertEqual(dog.status, 'l')
