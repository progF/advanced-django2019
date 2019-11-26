# import os
# from django.conf import settings
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from core.models import Project, TaskDocument
# from utils.constants import NEW,TO_DO,IN_PROGRESS,DONE


# @receiver(post_save, sender=Project, dispatch_uid="_uid")
# def create_blocks(sender, instance, created, **kwargs):
#     if created:
#         Block.objects.create(type=NEW, project=instance)
#         Block.objects.create(type=TO_DO, project=instance)
#         Block.objects.create(type=IN_PROGRESS, project=instance)
#         Block.objects.create(type=DONE, project=instance)


# @receiver(post_delete, sender=TaskDocument)
# def delete_task_document(sender,instance, **kwargs):
#     os.remove(instance.document.path)
