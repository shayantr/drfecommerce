from django.db import models

from core.models.base_model import BaseModel

class UserCart(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cart_user')
    class Meta:
        db_table = 'user_cart'

class Cart(BaseModel):
    cart = models.ForeignKey('UserCart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    class Meta:
        db_table = 'cart_item'
