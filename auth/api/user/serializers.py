from django.contrib.auth import authenticate, login
from django.core import validators
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User
from core.serializer import PhoneSerializer, StrongPasswordValidator


class RegisterSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer
    password = serializers.CharField(write_only=True, required=True, validators=[
        StrongPasswordValidator()
    ])
    password2 = serializers.CharField(write_only=True, required=True, validators=[
        StrongPasswordValidator()
    ])

    class Meta:
        model = User
        fields = ('phone', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return attrs

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

