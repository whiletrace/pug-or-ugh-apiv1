from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class Dogs(RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
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




