from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from django.shortcuts import get_object_or_404

from core.models import TaskDocument, Task, TaskComment
from core.serializers import ProjectSerializer, TaskDocumentSerializer, TaskCommentSerializer


class DocumentListViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,):

    serializer_class = TaskDocumentSerializer

    def get_queryset(self):
        documents = Task.objects.get(id=self.request.query_params['task']).documents
        return documents

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, task=Task.objects.get(id=self.request.query_params['task']))


class CommentListViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,):

    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        comments = Task.objects.get(id=self.request.query_params['task']).comments
        return comments

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, task=Task.objects.get(id=self.request.query_params['task']))
