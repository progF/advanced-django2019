import logging
from rest_framework import serializers
from core.models import Project, TaskComment, TaskDocument, Task, Block
from users.serializers import MainUserSerializer
from utils.constants import NEW
from users.models import MainUser
from django.shortcuts import get_object_or_404


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


class TaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'order')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class BlockSerializer(serializers.ModelSerializer):
    tasks = TaskShortSerializer(many=True)
    class Meta:
        model = Block
        fields = ('name', 'tasks')
        depth = 1


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
class TaskShortSerializer(serializers.Serializer):
    class Meta:
        model = Task
        fields = ('name', 'block', 'order')



class CreateTaskSerializer(serializers.Serializer):

    class Meta:
        model = Task
        fields = ('name', 'description', 'executor')

    def create(self, validated_data):
        creator = validated_data.get('creator')
        block = validated_data.get('block')
        order = validated_data.get('order')
        name = validated_data.get('name')
        description = validated_data.get('description')
        executor = get_object_or_404(MainUser, id=validated_data.get('executor'))
        task = Task.objects.create(
            name=name, description=description, executor=executor, block=block, order=order
        )
        return task


class TaskSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False)
    block = BlockSerializer(required=False)
    executor = MainUserSerializer()
    class Meta:
        model = Task
        fields = '__all__'


    def validate_executor(self, value):
        try:
            return MainUser.objects.get(id=value)
        except Exception:
            raise serializers.ValidationError("Not correct executor")
    # def create(self,validated_data):
    #     print(validated_data)
    #     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #     task = Task.objects.create(**validated_data)
    #     return task


# class TaskDocumentSerializer(serializers.Serializer):
#     creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     task = TaskSerializer(read_only=True)
#     class Meta:
#         model = TaskDocument
#         fields = ('__all__')


class TaskDocumentSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        document = TaskDocumentSerializer.objects.create(**validated_data)
        return document

    def update(self, instance, validated_data):
        instance.document = validated_data.get('document', instance.document)
        instance.task = validated_data.get('task', instance.task)
        instance.save()
        return instance

    # def validate_document(self, value):
    #     if len(value) >= 100:
    #         raise serializers.ValidationError('Name field must be max len: 100')
    #     return value

    # def validate_status(self, value):
    #     if int(value) > 3:
    #         raise serializers.ValidationError('Status options: [1, 2, 3]')
    #     return value

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