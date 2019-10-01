from rest_framework import serializers
from users.serializers import MainUserSerializer
from .models import (
    Project,
    ProjectMember,
    Block,
    Task,
    TaskComment,
    TaskDocument
)

class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=2000)
    creator = MainUserSerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = ('name', 'description', 'creator')


class ProjectMemberSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    user = MainUserSerializer()
    class Meta:
        model = ProjectMember
        fields = ('__all__')

class BlockSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = Block
        fields = ('__all__')


class TaskSerializer(serializers.ModelSerializer):
    creator = MainUserSerializer(read_only=True)
    executor = MainUserSerializer(required=False)
    block = BlockSerializer(read_only=True)
    order = serializers.IntegerField(read_only=True)
    class Meta:
        model = Task
        fields = ('__all__')

class TaskDocumentSerializer(serializers.Serializer):
    creator = MainUserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    class Meta:
        model = TaskDocument
        fields = ('__all__')

class TaskCommentSerializer(serializers.Serializer):
    creator = MainUserSerializer()
    task = TaskSerializer()
    class Meta:
        model = TaskComment
        fields = ('__all__')

