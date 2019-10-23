from rest_framework import serializers
from .models import MainUser


class MainUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'password')
    
    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = MainUser.objects.create_user(username, password)
        return user
