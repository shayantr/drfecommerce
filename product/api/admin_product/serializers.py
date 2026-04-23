from attr.validators import max_len
from django.core import validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from core.models import Product, ProductImage


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        image = serializers.ImageField(required=True, allow_null=False, validators=[validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'], message='file supported only jpg, jpeg and png')])
        model = ProductImage
        fields = ['image', 'main_image']
        # extra_kwargs = {'id': {'read_only': True}}

    def validate_image(self, value):
        if value.size > 1024000:
            raise ValidationError(detail='Image must be less than 1024 bytes', code='invalid')
        return value


class AdminProductSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), write_only=True)
    images_detail = serializers.PrimaryKeyRelatedField(many=True, source="images", read_only=True)
    title = serializers.CharField(trim_whitespace=True,
                                  validators=[validators.MinLengthValidator(1, "at least 1 character required!"),
                                              validators.MaxLengthValidator(100, "maximum 100 character or less!"),
                                              ])
    slug = serializers.CharField(trim_whitespace=True,
                                 validators=[UniqueValidator(queryset=Product.objects.all(), message="slug name must be unique"),
                                             ])
    price = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price', 'sku', "images", "images_detail"]
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        img = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        product.images.add(img)
        product.user = self.context['request'].user
        product.save()
        return product
