import os
import shutil

def avatar_path(instance, filename):
    profile = instance.user.username
    return f'avatars/{profile}/{filename}'

def avatar_delete_path(image):
    path = os.path.abspath(os.path.join(image.path, '..'))
    shutil.rmtree(path)

def document_path(instance, filename):
    project = instance.task.block.project.name
    block = instance.task.block.name
    return f'projects/{project}/{block}/{filename}'

def delete_task_path(document):
    path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(path)
