"""
Test for cart API
"""
from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from core.models import Cart, UserCart, Product

CART_URL = reverse("orders:cart")

def cart_detail_url(cart_id):
    return reverse("admin-orders:cart-detail", kwargs={'id':cart_id})

def create_user(phone='09180043744', password='12345!@#Asd'):
    """create and return user """
    return get_user_model().objects.create(phone=phone, password=password)

def create_user_cart(user, **kwargs):
    """create and return cart """
    return UserCart.objects.create(user=user)

def get_token_for_user(user):
    """get token for user """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def create_product(user, **kwargs):
    """create and return product """
    defaults = {
        "title": "pro12",
        "slug": "pro12",
        "description": "this is pro12",
        "price": 12,
        "sku": "sku-pro12"
    }
    defaults.update(**kwargs)
    return Product.objects.create(user=user, **kwargs)

class PrivateCartTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(get_token_for_user(self.user)))
