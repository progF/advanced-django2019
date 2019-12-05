import logging
from rest_framework import serializers
from core.models import Project, TaskComment, TaskDocument, Task, Block
from users.serializers import MainUserSerializer
from utils.constants import NEW
from users.models import MainUser
from django.shortcuts import get_object_or_404


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


class TaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'order')


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



class CreateTaskSerializer(serializers.ModelSerializer):
    block = BlockSerializer(required=False)
    order = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ('name', 'description', 'block', 'order', 'creator')

    # def create(self, validated_data):
    #     creator = validated_data.get('creator')
    #     block = validated_data.get('block')
    #     order = validated_data.get('order')
    #     name = validated_data.get('name')
    #     description = validated_data.get('description')
    #     task = Task.objects.create(
    #         name=name, description=description, block=block, order=order
    #     )
    #     return task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UpdateTaskSerializer(serializers.ModelSerializer):
    # creator = MainUserSerializer(required=False)
    # executor = MainUserSerializer(required=False)
    # block = BlockSerializer(required=False)

    class Meta:
        model = Task
        fields = '__all__'


    def get_fields(self):
        fields = super(UpdateTaskSerializer, self).get_fields()
        for field in fields.values():
            field.required = False
        return fields
    

    def update(self, instance, validated_data):
        orders = []
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.creator = validated_data.get('creator', instance.creator)
        instance.executor = validated_data.get('executor', instance.executor)
        if instance.block != validated_data.get('block'):
            instance.block = validated_data.get('block', instance.block)
            instance.order = instance.block.tasks.count()+1
        else:
            if validated_data.get('order'):
                old_order = instance.order
                instance.order = validated_data.get('order', instance.order)
                tasks = instance.block.tasks.all().order_by("order")
                for task in tasks:
                    orders.append(task)
                orders.insert(instance.order-1, orders.pop(old_order-1))
                for task in orders:
                    task.order = orders.index(task)+1
                    task.save()
        instance.save()
        return instance 

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