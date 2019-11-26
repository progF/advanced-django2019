from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import MainUser
from users.serializers import MainUserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins


class RegisterViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = MainUserSerializer
