from django.db import models
from django.contrib.auth.models import AbstractUser


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'

class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    address = models.CharField(max_length=300)
    avatar = models.ImageField(upload_to='images/')
    web_site = models.CharField(max_length=200)
