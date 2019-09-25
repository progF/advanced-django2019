from rest_framework import serializers
from .models import MainUser


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email',)

