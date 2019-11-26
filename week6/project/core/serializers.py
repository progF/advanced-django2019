import logging
from rest_framework import serializers
from core.models import Project
from users.serializers import MainUserSerializer


logger = logging.getLogger(__name__)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description')
        read_only_fields = ('creator',)

    def create(self,validated_data):
        project = None
        try:
            name = validated_data.get('name')
            description = validated_data.get('description')
            creator = self.context['request'].user
            project = Project.objects.create(name=name, description=description, creator=creator)
        except Exception:
            logger.error("Project couldnt be created")
            raise serializers.ValidationError("Required fields are not full")
        return project

# class ProjectMemberSerializer(serializers.ModelSerializer):
#     project_id = serializers.IntegerField()
#     user_id = serializers.IntegerField()

#     class Meta:
#         model = ProjectMember
#         fields = ('__all__')

# class BlockSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(read_only=True)
#     class Meta:
#         model = Block
#         fields = ('__all__')


# class TaskSerializer(serializers.ModelSerializer):
#     executor = MainUserSerializer(required=False)
#     block = BlockSerializer(read_only=True)
#     order = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Task
#         fields = ('__all__')
#         read_only_fields = ['creator']
#         optional_fields = ['executor',]


# class TaskDocumentSerializer(serializers.Serializer):
#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     task = TaskSerializer(read_only=True)
#     class Meta:
#         model = TaskDocument
#         fields = ('__all__')
