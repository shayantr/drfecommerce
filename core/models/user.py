from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager

from core.models.base_model import BaseModel

class Roles(models.IntegerChoices):
    CUSTOMER = 1, 'Customer'
    ADMIN = 2, 'Admin'
    ACCOUNTANT = 3, 'Accountant'

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('User must have phone number')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.role = Roles.CUSTOMER
        user.save(using=self._db)
        return user
    def create_superuser(self, phone, password=None, **extra_fields):
        user = self.create_user(phone, password, **extra_fields)
        user.is_staff = True
        user.role = Roles.ADMIN
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user'
        ordering = ['phone']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.IntegerField(choices=Roles.choices, default=Roles.CUSTOMER)

    USERNAME_FIELD = 'phone'


class UserAddress(BaseModel):
    class Meta:
        db_table = 'user_address'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    details = models.TextField()




