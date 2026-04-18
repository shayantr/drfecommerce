from django.db import models

from core.models.base_model import BaseModel
from core.models.choices import StockAvailability


class Product(BaseModel):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    stock_availability = models.IntegerField(choices=StockAvailability.choices, default=StockAvailability.YES)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    sku = models.CharField(max_length=256)

    class Meta:
        db_table = 'product'


class ProductImage(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='images')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Image', upload_to='product_images')
    main_image = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_image'
