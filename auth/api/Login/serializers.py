import re

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# phone_validator = RegexValidator(
#     regex=r'^0\d{10}$',
#     message='شماره تلفن باید دقیقا ۱۱ رقم و با صفر شروع شده باشد.'
# )

class AdminSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True, max_length=11, min_length=11, validators=[phone_validator])
    password = serializers.CharField(write_only=True)
    user = serializers.HiddenField(default=None)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate_phone(self, value):
        if not re.match(r'^0\d{10}$', value):
            raise serializers.ValidationError('شماره تلفن باید دقیقا ۱۱ رقم و با صفر شروع شده باشد.')
        return value


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
