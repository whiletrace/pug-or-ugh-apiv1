from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView, RetrieveUpdateAPIView, UpdateAPIView,
    )
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

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
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer

    def get_queryset(self):

        user = self.request.user
        preferences = models.UserPref.objects.get(user=user)
        age = preferences.get_age_display()
        gender = preferences.gender.split(',')
        size = preferences.size.split(',')
        status = self.kwargs['status']
        dogs = models.Dog.objects.filter(
            Q(age__in=age) & Q(size__in=size) & Q(gender__in=gender))
        if status == 'undecided':
            return dogs.filter(user_dogs_query__status='u',
                               user_dogs_query__user=user)
        elif status == 'liked':
            return dogs.filter(user_dogs_query__status='l',
                               user_dogs_query__user=user)
        elif status == 'disliked':
            return dogs.filter(user_dogs_query__status='d',
                               user_dogs_query__user=user)

    def get_object(self):

        queryset = self.get_queryset()

        try:
            dog = queryset.filter(pk__gt=self.kwargs["pk"])[0]
            return dog
        except IndexError:
            raise Http404


class UpdateStatus(UpdateAPIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        dogs = models.Dog.objects.filter(user_dogs_query__user_id=user_id)
        return dogs

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        pk = self.kwargs['pk']
        dog = queryset.filter(pk=pk).get().users_dog.select_related().filter(
            user=user).get()
        return dog

    def put(self, request, *args, **kwargs):
        status_filter = self.kwargs['status']
        dog = self.get_object()
        serializer = self.serializer_class(dog.dog)
        if status_filter == 'liked':
            dog.status = 'l'
            dog.save()
        if status_filter == 'disliked':
            dog.status = 'd'
            dog.save()
        if status_filter == 'undecided':
            if dog.status != 'u':
                dog.status = 'u'
                dog.save()

        return Response(serializer.data)
