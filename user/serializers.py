from django.contrib.auth import authenticate
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone')

class AdminSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            phone = attrs['phone'],
            password = attrs['password']
        )
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        if not user.auth_providers == 2:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs



