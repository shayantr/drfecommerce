from django.contrib.auth import authenticate
from rest_framework import serializers

from core.serializer import PhoneSerializer


class LoginSerializer(serializers.Serializer):
    phone = PhoneSerializer()
    password = serializers.CharField(write_only=True)
    user = serializers.HiddenField(default=None)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

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
        user = self.context['request'].user
        return user.get_token()