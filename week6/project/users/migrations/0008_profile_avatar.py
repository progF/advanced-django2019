# Generated by Django 2.2.5 on 2019-11-13 02:50

import django.core.validators
from django.db import migrations, models
import utils.file_upload


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=utils.file_upload.avatar_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
    ]
