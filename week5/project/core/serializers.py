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
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Project
        fields = ('name', 'creator')

    def validate_name(self, value):
        if len(value) >= 50:
            raise serializers.ValidationError('Name field must be max len: 50')
        return value

class ProjectFullSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('description',)


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
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    executor = MainUserSerializer(required=False)
    block = BlockSerializer(read_only=True)
    order = serializers.IntegerField(read_only=True)
    class Meta:
        model = Task
        fields = ('__all__')
        optional_fields = ['executor',]


class TaskDocumentSerializer(serializers.Serializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = TaskSerializer(read_only=True)
    class Meta:
        model = TaskDocument
        fields = ('__all__')

class TaskCommentSerializer(serializers.Serializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task = TaskSerializer()
    class Meta:
        model = TaskComment
        fields = ('__all__')

