from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models
from.models import GENDER_CHOICES, SIZE_CHOICES, AGE_CHOICES

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
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    size = serializers.ChoiceField(choices=SIZE_CHOICES)

    class Meta:
        model = models.Dog

        fields = ['name', 'image_filename', 'gender', 'size',
                  'breed', 'age', 'id']


class UserPrefSerializer(serializers.ModelSerializer):

    age = serializers.MultipleChoiceField(choices=AGE_CHOICES)
    gender = serializers.MultipleChoiceField(choices=GENDER_CHOICES)
    size = serializers.MultipleChoiceField(choices=SIZE_CHOICES)

    class Meta:
        model = models.UserPref
        exclude = ['user']


