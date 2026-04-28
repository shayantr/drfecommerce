import re

from django.contrib.auth import authenticate
from django.core import validators
from django.core.exceptions import ValidationError
from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
        validators=[
            validators.MinLengthValidator(11,'Phone number must be at least 11 characters long.'),
            validators.MaxLengthValidator(11,'Phone number cant be more than 11 characters long.'),
            validators.RegexValidator(r'^0\d{10}$','Phone number must start with 0'),
        ])


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            validators.RegexValidator(r'[A-Z]', 'At least one character must be Capitalized.'),
            validators.RegexValidator(r'[a-z]', 'At least one character must be Small.'),
            validators.RegexValidator(r'\d', 'At least one character must be Digit.'),
            validators.RegexValidator(r'[!@#$%^&*(),.?":{}|<>]', 'At least one character must be Special Character.'),
            validators.MinLengthValidator(8, 'Password must have at least 8 characters.'),
            validators.MaxLengthValidator(32, 'Password must be less than least 32 characters.'),
        ])

