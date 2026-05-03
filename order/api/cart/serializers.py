from django.db import transaction
from rest_framework import serializers

from core.models import Cart, UserCart, Product

class FinalPriceSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        representation = super(FinalPriceSerializer, self).to_representation(instance)
        final_price = sum(i['total_price'] for i in representation)
        representation.append({'final_price': final_price})
        return representation


class AddToCartSerializer(serializers.ModelSerializer):
    cart = serializers.CharField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = ["id", "cart", "product", "quantity", "total_price"]
        extra_kwargs = {"id": {"read_only": True}}
        list_serializer_class = FinalPriceSerializer

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

    def validate_product(self, product):
        if product.quantity < 1:
            raise serializers.ValidationError("Quantity must be greater than 0!")
        elif not product.stock_availability or not product.is_active:
            raise serializers.ValidationError("Stock must be available")
        return product

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

    def update(self, instance, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        if quantity > product.quantity:
            raise serializers.ValidationError("Quantity must be less than product quantity")
        else:
            instance.quantity = quantity
            instance.save()
        return instance

