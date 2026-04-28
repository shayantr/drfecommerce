from django.contrib.auth import authenticate, login
from django.core import validators
from rest_framework import serializers, status
from core.models import User
from core.serializer import PhoneSerializer, PasswordSerializer


class RegisterSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer()
    password = PasswordSerializer()
    password_2 = PasswordSerializer()

    class Meta:
        model = User
        fields = ('phone', 'password', 'password_2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError('Passwords must match.')
        return attrs

    def create(self, validated_data):
        password_2 = validated_data.pop('password_2')
        user = User.objects.create_user(**validated_data)
        return user
