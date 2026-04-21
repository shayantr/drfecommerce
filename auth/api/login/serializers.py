from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


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
        if user.role != 2:
            raise serializers.ValidationError('unauthorized user')
        attrs['user'] = user
        return attrs

    def _get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    def create(self, validated_data):
        user = validated_data['user']
        return self._get_tokens(user)
