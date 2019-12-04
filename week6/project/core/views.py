from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.models import Project, Task, Block
from users.models import MainUser
from core.serializers import (
    ProjectSerializer,
    TaskShortSerializer,
    TaskSerializer,
    BlockSerializer,
    CreateTaskSerializer,
    TaskDocumentSerializer,
    TaskCommentSerializer
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


class DocumentListViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = TaskDocumentSerializer

    def get_queryset(self):
        documents = Task.objects.get(id=self.request.query_params['task']).documents
        return documents

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, task=Task.objects.get(id=self.request.query_params['task']))


class CommentListViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        comments = Task.objects.get(id=self.request.query_params['task']).comments
        return comments

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, task=Task.objects.get(id=self.request.query_params['task']))