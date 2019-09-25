from rest_framework import serializers
from users.serializers import MainUserSerializer
from .models import (
    Project,
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


class BlockSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model = Block
        fields = ('__all__')
