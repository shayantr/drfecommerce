from rest_framework import serializers

from core.models import Product, ProductImage


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'main_image']
        extra_kwargs = {'id': {'read_only': True}}


class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price', 'sku']
        extra_kwargs = {'id': {'read_only': True}}

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Title is required')
        return value.strip(" ")

    def validate_description(self, value):
        if value is None:
            raise serializers.ValidationError('Description is required')
        return value

    def validate_price(self, value):
        if value == 0:
            raise serializers.ValidationError('Price is required or cant be 0!')
        return value

    def validate_sku(self, value):
        if not value:
            raise serializers.ValidationError('SKU is required')
        return value



    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product.user = self.context['request'].user
        product.save()
        return product
