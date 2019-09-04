from rest_framework import serializers
from api.models import Review, Product
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'