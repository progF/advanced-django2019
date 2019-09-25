from django.db import models
from user.models import MainUser
from utils.constants import BLOCK_TYPES, NEW

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)


class Block(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(choices=BLOCK_TYPES, default=NEW, max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='creator')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='executor')
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    

class TaskDocument(models.Model):
    document = models.FileField(upload_to='documents/')
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class TaskComment(models.Model):
    body = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)





