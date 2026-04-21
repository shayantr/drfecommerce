from rest_framework import serializers

from core.models import Product, ProductImage


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'main_image']

class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'description', 'price', 'sku']


    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product.user = self.context['request'].user
        product.save()
        return product


