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


class Dogs(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        """

        :return:
        :rtype:
        """
        queryset = self.get_queryset()
        next_dog = queryset.filter(pk__gt=self.kwargs['pk'])[:1].get()
        return next_dog


class CreateUpdatePreference(RetrieveModelMixin, UpdateModelMixin,
                             GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
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












