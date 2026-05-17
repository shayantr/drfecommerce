from rest_framework import serializers

from core.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parent_id = serializers.IntegerField(source='parent.id', allow_null=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id','user', 'name', 'parent_id']
