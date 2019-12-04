from django.contrib import admin
from core.models import Project, Task, TaskDocument, Block

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskDocument)
admin.site.register(Block)