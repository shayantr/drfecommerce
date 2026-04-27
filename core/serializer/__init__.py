import re

from django.contrib.auth import authenticate
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True, trim_whitespace=True,
                                  validators=[validators.MinLengthValidator(11,
                                                                            'شماره تلفن کمتر از ۱۱ رقم نمیتواند باشد!'),
                                              validators.MaxLengthValidator(11,
                                                                            'شماره تلفن بیشتر از ۱۱ رقم نمیتواند باشد!'),
                                              validators.RegexValidator(r'^0\d{10}$',
                                                                        'شماره تلفن باید دقیقا ۱۱ رقم و با صفر شروع شده باشد.'), ])



class StrongPasswordValidator:
    def __call__(self, value):
        self.validate(value)
    def validate(self, password):
        if len(password) < 8:
            raise ValidationError("رمز عبور نباید کمتر از ۸ حرف باشد")
        if len(password) > 32:
            raise ValidationError("رمز عبور نباید بیشتر از ۳۲ حرف باشد.")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('حداقل یک حرف بزرگ برای رمز عبور نیاز است.')

        if not re.search(r'[a-z]', password):
            raise ValidationError('حداقل یک حرف کوچک برای رمز عبور نیاز است.')

        if not re.search(r'\d', password):
            raise ValidationError('حداقل یک عدد برای رمز عبور نیاز است')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('حداقل یک کاراکتر خاص برای رمز عبور نیاز است.')

    def get_help_text(self):
        return "رمز عبور باید شامل حرف بزرگ و کوچک به همراه عدد و یک کاراکتر خاص باشد."

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