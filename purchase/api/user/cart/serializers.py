from django.db import transaction
from django.db.models import Sum, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from core.models import Cart, UserCart


class AddToCartSerializer(serializers.ModelSerializer):
    cart = serializers.CharField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = ["id", "cart", "product", "quantity", "total_price"]
        extra_kwargs = {"id": {"read_only": True}}

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_price(self, obj):
        return obj.total_price

    def validate_product(self, product):
        if product.quantity < 1:
            raise serializers.ValidationError("Quantity must be greater than 0!")
        elif not product.stock_availability or not product.is_active:
            raise serializers.ValidationError("Stock must be available")
        return product

    def validate_quantity(self, qty):
        if qty == 0:
            raise serializers.ValidationError("Quantity cannot be 0!")
        return qty

    def validate(self, attrs):
        product = attrs["product"]
        quantity = attrs["quantity"]
        if quantity > product.quantity:
            raise serializers.ValidationError("Quantity must be less than product quantity")
        return attrs

    def create(self, validated_data):
        user_cart = UserCart.objects.get_or_create(user=self.context['request'].user)
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        with transaction.atomic():
            if Cart.objects.filter(cart=user_cart[0], product=product).exists():
                item = Cart.objects.select_for_update().get(cart=user_cart[0], product=product)
                quantity = quantity + item.quantity
                if quantity > product.quantity:
                    raise serializers.ValidationError("Quantity must be less than product quantity")
                else:
                    item.quantity = quantity
                    item.save()
            else:
               item = Cart.objects.create(cart=user_cart[0], product=product, quantity=quantity)
        return item


class UpdateCartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    product = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = Cart
        fields = ["id", "product", "quantity", "total_price"]
        extra_kwargs = {"id": {"read_only": True}, "product": {"read_only": True}}

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_price(self, obj):
        return obj.total_price

    def validate_quantity(self, quantity):
        product = self.instance.product
        if quantity == 0:
            raise serializers.ValidationError("Quantity cannot be 0!")
        if quantity > product.quantity:
            raise serializers.ValidationError("Quantity must be less than product quantity")
        return quantity

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity')
        instance.save()
        return instance

class ListCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = UpdateCartSerializer(source='items',many=True, read_only=True)
    final_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserCart
        fields = ['user', 'cart_items', 'final_price']

    @extend_schema_field(OpenApiTypes.INT)
    def get_final_price(self, obj):
        return obj.items.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total']


