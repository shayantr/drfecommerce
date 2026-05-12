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

    def validate_image(self, value):
        if value.size > 1024000:
            raise ValidationError(detail='Image must be less than 1024 bytes', code='invalid')
        return value


class AdminProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), write_only=True, required=False)
    images_detail = serializers.PrimaryKeyRelatedField(many=True, source="images", read_only=True)
    title = serializers.CharField(trim_whitespace=True,
                                  validators=[validators.MinLengthValidator(1, "at least 1 character required!"),
                                              validators.MaxLengthValidator(100, "maximum 100 character or less!"),
                                              ])
    slug = serializers.CharField(trim_whitespace=True,
                                 validators=[UniqueValidator(queryset=Product.objects.all(), message="slug name must be unique"),
                                             ])
    price = serializers.IntegerField()
    sale_price = serializers.IntegerField(required=False, allow_null=True, default=None)
    class Meta:
        model = Product
        fields = ['id','user', 'title', 'slug', 'description', 'price', 'sale_price', 'sku', "images", "images_detail"]
        extra_kwargs = {'id': {'read_only': True}}

    def validate_sale_price(self, sale_price):
        if sale_price < 1:
            sale_price = None
        return sale_price
    def validate_price(self, price):
        if price < 1:
            price = None
        return price

    def create(self, validated_data):
        img = validated_data.pop('images', None)
        product = Product.objects.create(**validated_data)
        if img:
            product.images.add(img)
        product.save()
        return product
