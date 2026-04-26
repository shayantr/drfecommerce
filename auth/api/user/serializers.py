from django.contrib.auth import authenticate, login
from django.core import validators
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True, trim_whitespace=True,
                                  validators=[validators.MinLengthValidator(11,
                                                                            'phone number length must be 11 characters at least!'),
                                              validators.MaxLengthValidator(11,
                                                                            'phone number length must be 11 characters maximum!'),
                                              validators.RegexValidator(r'^0\d{10}$',
                                                                        'شماره تلفن باید دقیقا ۱۱ رقم و با صفر شروع شده باشد.'), ])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('phone', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return attrs

    def create(self, validated_data):
        phone = validated_data['phone']
        password = validated_data['password']
        user = User(phone=phone, password=password, role=1)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True, trim_whitespace=True,
                                  validators=[validators.MinLengthValidator(11,
                                                                            'phone number length must be 11 characters at least!'),
                                              validators.MaxLengthValidator(11,
                                                                            'phone number length must be 11 characters maximum!'),
                                              validators.RegexValidator(r'^0\d{10}$',
                                                                        'شماره تلفن باید دقیقا ۱۱ رقم و با صفر شروع شده باشد.'), ])
    password = serializers.CharField(write_only=True)
    user = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(phone=phone, password=password)
        if user is None:
            raise serializers.ValidationError('invalid username or password')
        attrs['user'] = user
        return attrs

    def _get_tokens(self):
        refresh = RefreshToken.for_user(self.validated_data.get('user'))
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': self.validated_data.get('user'),
            'role': self.validated_data.get('user').role,
        }

    def create(self, validated_data):
        return self._get_tokens()
