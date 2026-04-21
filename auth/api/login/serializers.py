from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class AdminSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True)
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
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs

    def _get_tokens(self):
        refresh = RefreshToken.for_user(self.validated_data.get('user'))
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    def create(self, validated_data):
        return self._get_tokens()
