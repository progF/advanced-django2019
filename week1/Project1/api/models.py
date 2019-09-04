from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class ReviewManager(models.Manager):
    def for_user(self,user):
        return self.filter(user=user)
    

class Product(models.Model):
    rating = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return '{}:{}'.format(self.id,self.name)
    
    def to_json(self):
        return {
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'rating':self.rating
        }



class Review(models.Model):
    rating = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    title=models.CharField(max_length=200)
    summary=models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    photo = models.ImageField(upload_to='images/')
    objects=ReviewManager()

    def __str__(self):
        return '{}:{}'.format(self.id,self.title)
    
    def to_json(self):
        return {
            'id':self.id,
            'title':self.title,
            'summary':self.summary,
            'date':self.date,
            'user':self.user,
        }
