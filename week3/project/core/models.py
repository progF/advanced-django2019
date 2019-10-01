from django.db import models
from users.models import MainUser
from utils.constants import BLOCK_TYPES, NEW

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='projects')


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)


class Block(models.Model):
    name = models.CharField(max_length=200)
    type = models.IntegerField(choices=BLOCK_TYPES, default=NEW)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='blocks')


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.SET_NULL, related_name='creator_tasks', null=True)
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='executor_tasks', null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='tasks')
    order = models.IntegerField(unique=True)
    

class TaskDocument(models.Model):
    document = models.FileField(upload_to='documents/')
    creator = models.ForeignKey(MainUser, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')

class TaskComment(models.Model):
    body = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')