from rest_framework import serializers

from core.models import UserAddress


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserAddress
        fields = ["id", "user", "name", "last_name", "street", "city", "province", "post_code", "details"]
        extra_kwargs = {'id': {'read_only': True}}

class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ["city", "street", "details"]
