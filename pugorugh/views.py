from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import CreateAPIView, \
    GenericAPIView, RetrieveUpdateAPIView
from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class CreateUpdatePreference(RetrieveModelMixin, UpdateModelMixin,
                             GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        """

        :return:
        :rtype:

        """
        queryset = self.get_queryset()
        user = self.request.user

        try:
            return queryset.filter(user=user).get()
        except models.UserPref.DoesNotExist:
            return models.UserPref.objects.create(user=user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class Dogs(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    @staticmethod
    def convert_age(dogs):
        for dog in dogs:
            age_attr = getattr(dog, "age")
            if age_attr in range(0, 6):
                setattr(dog, 'age', 'b')
                yield dog
            elif age_attr in range(7, 18):
                setattr(dog, 'age', 'y')
                yield dog
            elif age_attr in range(19, 36):
                setattr(dog, 'age', 'a')
                yield dog
            else:
                setattr(dog, 'age', 's')
                yield dog

    def get_object(self):
        """

        :return:
        :rtype:
        """

        queryset = self.get_queryset()
        test = self.convert_age(queryset)
        user = self.request.user
        age = user.userprefs.get().age.split(',')
        gender = user.userprefs.get().gender.split(',')
        size = user.userprefs.get().size.split(',')
        filtered_dog = test.filter(gender__in=gender).filter(size__in=size)
        try:
            return queryset.filter(user=user, dog=filtered_dog).get()
        except models.UserDog.DoesNotExist:
            return models.UserDog.objects.create(user=user, dog=filtered_dog)
















