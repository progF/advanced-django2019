from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from core.models import Project, Task, Block, TaskDocument, TaskComment
from users.models import MainUser
from core.serializers import (
    ProjectSerializer,
    TaskShortSerializer,
    TaskSerializer,
    BlockSerializer,
    CreateTaskSerializer,
    TaskDocumentSerializer,
    TaskCommentSerializer,
    UpdateTaskSerializer
)
from core.models import Project
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.decorators import (api_view,
                                       permission_classes)
from utils.constants import NEW
from core.permissions import UserPermissions
from django.http import Http404
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_blocks_by_project(request):
    project_id = request.query_params.get('project_id')
    project = get_object_or_404(Project, id=project_id)
    if request.user == project.creator or request.user.id in project.members__id:
        blocks = Block.objects.filter(project=project)
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)  # noqa
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_task(request):
    project_id = request.query_params.get('project_id')
    project = get_object_or_404(Project, id=project_id)
    block = Block.objects.get(project=project, block_type=NEW)
    order = block.tasks.count()+1
    if request.user == project.creator or request.user.id in project.members__id:
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                block=block,
                order=order)
            return Response(serializer.data)
        return Response(serializer.errors)
    return Response(status=status.HTTP_403_FORBIDDEN)


class TaskDetailAPIView(APIView):
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, UserPermissions, )

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = UpdateTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        orders = []
        old_order = task.order
        tasks = task.block.tasks.all().order_by("order")
        for t in tasks:
            orders.append(t)
        orders.remove(task)
        task.delete()
        for t in orders:
            t.order = orders.index(t)+1
            t.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentListViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = TaskDocumentSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticatedOrReadOnly, UserPermissions, )
    def get_queryset(self):
        task = Task.objects.get(id=self.request.query_params['task'])
        documents = TaskDocument.objects.filter(task=task)
        return documents

    def perform_create(self, serializer):
        print(self.request.FILES)
        serializer.save(creator=self.request.user, task=Task.objects.get(id=self.request.query_params['task']))


class CommentListViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = TaskCommentSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    permission_classes = (IsAuthenticatedOrReadOnly, UserPermissions, )

    def get_queryset(self):
        task = Task.objects.get(id=self.request.query_params['task'])
        comments = TaskComment.objects.filter(task=task)
        return comments

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, task=Task.objects.get(id=self.request.query_params['task']))
