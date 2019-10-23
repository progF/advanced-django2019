from django.contrib import admin
from .models import (
    Project,
    ProjectMember,
    Block,
    Task,
    TaskDocument,
    TaskComment
)

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(Block)
admin.site.register(Task)
admin.site.register(TaskDocument)
admin.site.register(TaskComment)
