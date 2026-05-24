from django.db import models

from core.models.base_model import BaseModel

class UserCart(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cart_user')
    class Meta:
        db_table = 'user_cart'

class Cart(BaseModel):
    user_cart = models.ForeignKey('UserCart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    class Meta:
        db_table = 'cart'

    @property
    def total_price(self):
        if self.product.sale_price:
            return self.quantity * self.product.sale_price
        else:
            return self.quantity * self.product.price
