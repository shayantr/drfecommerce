from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('User must have phone number')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, password=None, **extra_fields):
        user = self.create_user(phone, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    class Meta:
        db_table = 'user'
        ordering = ['phone']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_address'

class order(models.Model):
    STATUS_CHOICES=(
    ('cancelled', 'Cancelled'),
    ('pending', 'Pending'),
    ('returned', 'Returned'),
    ('completed', 'Completed'),
    ('delivered', 'Delivered'),
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending'),
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    total_amount = models.IntegerField()
    address = models.ForeignKey('UserAddress', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    user = models.ForeignKey('user', on_delete=models.CASCADE)
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey('order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_order'

class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    stock_availability = models.CharField()
    images = models.ManyToManyField('ProductImage', blank=True)

    class Meta:
        db_table = 'product'


class ProductImage(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Image', upload_to='product_images')
    main_image = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_image'

class Basket(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    class Meta:
        db_table = 'basket'

class BasketItem(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        db_table = 'basket_item'

class Payment(models.Model):
    STATUS_CHOICES=(
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
        ('success', 'Success')

    )
    order = models.ForeignKey('order', on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=10)
    ip_address = models.IPAddressField()
    transaction_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'payment'


