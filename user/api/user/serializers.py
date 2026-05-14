from rest_framework import serializers

from core.models import UserAddress


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ["city", "street", "details"]
