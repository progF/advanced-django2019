from rest_framework import serializers
from .models import MainUser
from utils.functions import val_pass


class MainUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = MainUser.objects.create_user(
            username=username,
            password=password,
        )
        return user

    def validate_password(self, value):
        if len(value)<8:
            raise serializers.ValidationError('Password has to contain more that 8 characters.')
        if not val_pass(value):
            raise serializers.ValidationError('Password has to contain at least one digit.')
