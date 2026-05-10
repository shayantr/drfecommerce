"""
Test for cart API
"""
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from core.models import Cart, UserCart, Product
from order.api.user.cart import AddToCartSerializer

CART_URL = reverse("orders:carts-list")

def cart_detail_url(cart_id):
    return reverse("orders:carts-detail", kwargs={'pk':cart_id})

def create_user(phone='09181043742', password='12345!@#Asd'):
    """create and return user """
    return get_user_model().objects.create_user(phone=phone, password=password)

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
        "title": "pro1234242",
        "slug": "slug-product",
        "description": "this is pro12",
        "price": 125000,
        "quantity": 5,
        "sku": "sku-pro122323"
    }
    defaults.update(kwargs)
    return Product.objects.create(user=user, **defaults)

class PrivateCartTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(f'09380043744', 'ASDFfedsgrg@124')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(get_token_for_user(self.user)))

    def test_add_to_cart(self):
        product = create_product(user=self.user)
        payload = {
            'product': product.id,
            'quantity': 2,
        }
        res = self.client.post(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        cart = Cart.objects.first()
        s1 = AddToCartSerializer(cart)
        self.assertEqual(res.data, s1.data)

    def test_update_cart(self):
        product = create_product(user=self.user)
        user_cart = create_user_cart(self.user)
        cart = Cart.objects.create(cart=user_cart, product=product, quantity=2)
        payload = {
            'quantity': 1,
        }
        detail_url = cart_detail_url(cart.id)
        res = self.client.put(detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_cart(self):
        product = create_product(user=self.user)
        user_cart = create_user_cart(self.user)
        cart = Cart.objects.create(cart=user_cart, product=product, quantity=2)
        url = cart_detail_url(cart.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(id=cart.id).exists(), 0)

    def test_add_zero_quantity(self):
        product = create_product(user=self.user)
        user_cart = create_user_cart(self.user)
        payload = {
            'product': product.id,
            'quantity': 0,
            'cart': user_cart.id,
        }
        res = self.client.post(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Cart.objects.filter(id=user_cart.id).exists(), 0)

    def test_quantity_invalid(self):
        product = create_product(user=self.user)
        user_cart = create_user_cart(self.user)
        payload = {
            'product': product.id,
            'quantity': 6,
            'cart': user_cart.id,
        }
        res = self.client.post(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Cart.objects.filter(id=user_cart.id).exists(), 0)
