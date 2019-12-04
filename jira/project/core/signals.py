import os
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Project, TaskDocument, Block
from utils.constants import NEW,TO_DO,IN_PROGRESS,DONE
from utils.file_upload import delete_task_path

@receiver(post_save, sender=Project, dispatch_uid="_uid")
def create_blocks(sender, instance, created, **kwargs):
    if created:
        Block.objects.create(block_type=NEW, project=instance, name='New tasks')
        Block.objects.create(block_type=TO_DO, project=instance, name = 'To do tasks')
        Block.objects.create(block_type=IN_PROGRESS, project=instance, name ='Tasks in progress')
        Block.objects.create(block_type=DONE, project=instance, name='Done tasks')


@receiver(post_delete, sender=TaskDocument)
def delete_document(sender, instance, **kwargs):
    delete_task_path(instance.document)