from rest_framework import serializers

from core.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='image', read_only=True)

    class Meta:
        model = ProductImage
        fields = ('url', 'main_image')


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["title", "slug", "price", "stock_availability", "image_url"]

    def get_image_url(self, obj):
        image = obj.images.filter(main_image=True).first()
        return ProductImageSerializer(image).data.get('url') if image else None


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["title", "slug", "price",
                  "quantity", "stock_availability",
                  "sku", "description", 'images']
