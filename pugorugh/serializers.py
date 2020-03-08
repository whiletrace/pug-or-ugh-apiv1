from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            )

        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = '__all__'


class DogSerializer(serializers.ModelSerializer):

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
        (X_LARGE, 'ExtraLarge'),
        (UNKNOWN, 'Unknown')
        ]

    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    size = serializers.ChoiceField(choices=SIZE_CHOICES)

    class Meta:
        model = models.Dog

        fields = ['name', 'image_filename', 'gender', 'size',
                  'breed', 'age', 'id']


class UserPrefSerializer(serializers.ModelSerializer):
    age = serializers.CharField()
    gender = serializers.CharField()
    size = serializers.CharField()

    class Meta:
        model = models.UserPref
        exclude = ['user']
