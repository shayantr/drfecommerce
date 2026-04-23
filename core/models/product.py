import os
import uuid

from django.db import models
from django.utils.text import slugify

from app import settings
from core.models.base_model import BaseModel

def image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'media', filename)

class Product(BaseModel):
    class Meta:
        db_table = 'product'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    stock_availability = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    sku = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)




class ProductImage(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='images')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = models.ImageField(verbose_name='Image', upload_to=image_path)
    main_image = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_image'
