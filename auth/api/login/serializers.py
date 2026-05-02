from django.contrib.auth import authenticate
from rest_framework import serializers

from core.serializer import PasswordFieldSerializer, PhoneFieldSerializer


class LoginSerializer(serializers.Serializer):
    phone = PhoneFieldSerializer()
    password = serializers.CharField(write_only=True)
    user = serializers.CharField(read_only=True, default=None)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(
            phone=attrs['phone'],
            password=attrs['password']
        )
        if user is None:
            raise serializers.ValidationError('ورود نا معتبر')
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        return user.get_token()