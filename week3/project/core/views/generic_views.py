from rest_framework import generics
from rest_framework import mixins
from core.models import Block, Project, Task
from rest_framework.response import Response
from core.serializers import ProjectSerializer, BlockSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from users.models import MainUser
from core.permissions import IsOwner


class BlockListView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):

    
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticated,IsOwner)


    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs.get('pk'))
        queryset = project.blocks
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BlockDetailAPIView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):

    serializer_class = BlockSerializer

    def get_object(self):
        project = Project.objects.get(id=self.request.query_params['project'])
        block = project.blocks.get(type=self.kwargs.get('type'))
        return block

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class TaskListView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
                         
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        project = Project.objects.get(id=self.request.query_params['project'])
        block = project.blocks.get(type=self.kwargs.get('type'))
        queryset = block.tasks
        return queryset

    def perform_create(self, serializer):
        creator = self.request.user
        block = Block.objects.get(type=self.request.query_params['pk'])
        try:
            executor = MainUser.objects.get(id=self.request.data.get('executor'))
        except MainUser.DoesNotExist:
            executor = None
        if serializer.is_valid():
            serializer.save(creator=creator, executor=executor, block=block)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskDetailAPIView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self):
        task = self.queryset.get(id=self.kwargs.get('id'))
        return task

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
