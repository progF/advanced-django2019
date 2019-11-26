from django.db import models
from users.models import MainUser
from utils.constants import BLOCK_TYPES, NEW
from utils.file_upload import document_path

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='created_projects')
    members = models.ManyToManyField(MainUser, related_name='projects')


# class ProjectMember(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     member = models.ForeignKey(MainUser, on_delete=models.CASCADE)


# class Block(models.Model):
#     name = models.CharField(max_length=200, blank=True)
#     type = models.IntegerField(choices=BLOCK_TYPES, default=NEW)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='blocks')

#     class Meta:
#         verbose_name = "Block"
#         verbose_name_plural = "Blocks"

#     def __str__(self):
#         return self.name


# class Task(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(max_length=1000)
#     creator = models.ForeignKey(MainUser, on_delete=models.SET_NULL, related_name='creator_tasks', null=True)
#     executor = models.ForeignKey(MainUser, on_delete=models.SET_NULL, related_name='executor_tasks', null=True)
#     block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='tasks')
#     order = models.IntegerField(unique=True)

#     class Meta:
#         verbose_name = "Task"
#         verbose_name_plural = "Tasks"

#     def __str__(self):
#         return self.name


# class TaskDocument(models.Model):
#     document = models.FileField(upload_to=document_path)
#     creator = models.ForeignKey(MainUser, on_delete=models.SET_NULL, null=True)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')

#     class Meta:
#         verbose_name = "Document"
#         verbose_name_plural = "Documents"