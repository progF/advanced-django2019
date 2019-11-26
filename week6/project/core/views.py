from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.models import Project
from users.models import MainUser
from core.serializers import ProjectSerializer
from core.models import Project
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action


class ProjectViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(Q(creator=self.request.user)|Q(members__id=self.request.user.id))
        return queryset

class ProjectDetailViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)
