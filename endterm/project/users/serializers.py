import logging
from rest_framework import serializers
from users.models import MainUser, Profile

logger = logging.getLogger('__name__')
print(logger)

class MainUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'password')

    def create(self,validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = MainUser.objects.create_user(
            username = username.lower(),
            password = password
        )
        return user

    def validate_password(self,value):
        if len(value)<8:
            logging.error("PASSWORD IS NOT ALLOWABLE")
            raise serializers.ValidationError('Password has to contain more than 8 characters.')
        return value

    def validate_username(self,value):
        if MainUser.objects.filter(username=value.lower()):
            raise serializers.ValidationError('This username already exists.')
        return value

class ProfileSerializer(serializers.ModelSerializer):
    user = MainUserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
