from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

# Create your models here.
class MainUserManager(models.Manager):
    def create_user(self,username,email,password, **extra_fields):
        


class MainUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BigAutoField(default=False)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f'{self.id}: {self.username}'

class Profile(models.Model):
    info = models.TextField(max_length=600)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
