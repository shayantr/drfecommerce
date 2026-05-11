from django.core import validators
from rest_framework import serializers


class PhoneFieldSerializer(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('required', True)
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('trim_whitespace', True),
        kwargs.setdefault('validators', [
            validators.MinLengthValidator(11, 'Phone number must be at least 11 characters long.'),
            validators.MaxLengthValidator(11, 'Phone number cant be more than 11 characters long.'),
            validators.RegexValidator(r'^09\d{9}$', 'Phone number must start with 0'),
        ])
        super(PhoneFieldSerializer, self).__init__(**kwargs)


class PasswordFieldSerializer(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('required', True)
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('trim_whitespace', False),
        kwargs.setdefault('style', {'input_type': 'password'})
        kwargs.setdefault('validators', [
            validators.RegexValidator(r'[A-Z]', 'At least one character must be Capitalized.'),
            validators.RegexValidator(r'[a-z]', 'At least one character must be Small.'),
            validators.RegexValidator(r'\d', 'At least one character must be Digit.'),
            validators.RegexValidator(r'[!@#$%^&*(),.?":{}|<>]', 'At least one character must be Special Character.'),
            validators.MinLengthValidator(8, 'Password must have at least 8 characters.'),
            validators.MaxLengthValidator(32, 'Password must be less than least 32 characters.'),
        ])
        super(PasswordFieldSerializer, self).__init__(**kwargs)
