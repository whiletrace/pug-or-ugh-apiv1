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
    """
    Class responsible for logic for user Registration At  'api/user/'.

    subclasses rest_framework.generics.CreateAPIView

    Attr-Overrides:
        permission_classes

        model

        serializer_class

        See `DRF_GenericApiView <https://www.django-rest-framework.org/api-guide
        /generic-views/#genericapiview>`_ for info
    """
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class CreateUpdatePreference(RetrieveModelMixin, UpdateModelMixin,
                             GenericAPIView):
    """
    Class for retrieval, creation, update for 'api/user/preferences/'.

    subclasses rest_framework.generics.CreateAPIView, RetrieveModelMixin,
    UpdateModelMixin

    Attr overrides:
        permission_classes

        queryset

        serializer_class
    method overrides:
        get_object()

        See `DRF_GenericApiView <https://www.django-rest-framework.org/api
        -guide/ generic-views/#genericapiview>`_ for info
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        """
        retrieves or creates UserPref object for current user

        :rtype: object

        """
        queryset = self.get_queryset()
        user = self.request.user

        try:
            return queryset.filter(user=user).get()

        except models.UserPref.DoesNotExist:
            return models.UserPref.objects.create(user=user)

    def get(self, request, *args, **kwargs):
        """
            method that returns model instance of UserPref in response

            See `DRF_RetrieveModelMixin <https://www.django-rest-framework.org/
            api-guide/generic-views/#retrievemodelmixin>`_ for info
        """

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
            implements updating and saving an UserPref model instance.

            See `DRF_RetrieveModelMixin <https://www.django-rest-framework.org/
            api-guide/generic-views/#updatemodelmixin>`_ for info
        """
        return self.update(request, *args, **kwargs)


class Dogs(RetrieveUpdateAPIView):
    """
    Class for retrieval operations for 'api/dog/<pk>/<conv:status>/next/'.

    subclasses rest_framework.generics.RetrieveUpdateAPIView,

    Attr overrides:
            permission_classes

            serializer_class
    method overrides:
            get_queryset

            get_object

    See `DRF_RetrieveUpdateAPIView <https://www.django-rest-framework.org/
    api-guide/generic-views/#retrieveupdateapiview>`_ for info
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        """
        logic for initial filtration of QuerySet by UserPref attribute values

        filters initial queryset by UserPref.age, UserPref.size, UserPref.gender
        additional filters by URL keyword status
        """
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
        """returns Dog object or raises Http404 """
        queryset = self.get_queryset()

        try:
            dog = queryset.filter(pk__gt=self.kwargs["pk"])[0]
            return dog
        except IndexError:
            raise Http404


class UpdateStatus(UpdateAPIView):
    """
    Class for update operations for 'api/dog/<pk>/<conv:status>/'.

    subclasses rest_framework.generics.UpdateAPIView,

    Attr overrides:
            permission_classes

            serializer_class
    method overrides:
            get_queryset

            get_object

            put

    See `DRF_UpdateAPIView <https://www.django-rest-framework.org/api-guide
    /generic-views/#updateapiview>`_ for info
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        """filter initial queryset returns all dogs related to request.user"""
        user_id = self.request.user.id
        dogs = models.Dog.objects.filter(user_dogs_query__user_id=user_id)
        return dogs

    def get_object(self):
        """
        Returns UserDog object to be updated.

        from queryset filter related UserDog keyword arguments 'pk'
        passed by the URL

        """
        queryset = self.get_queryset()
        user = self.request.user
        pk = self.kwargs['pk']
        dog = queryset.filter(pk=pk).get().users_dog.select_related().filter(
            user=user).get()
        return dog

    def put(self, request, *args, **kwargs):
        """update UserDog.status object returns related serialized dog object"""
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
