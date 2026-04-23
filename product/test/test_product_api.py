"""
tests for product APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

import os, tempfile
from PIL import Image
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Product

PRODUCT_URL = reverse('product:product-list')


def detail_url(slug):
    """Return the url for product detail view"""
    return reverse('product:product-detail', kwargs={'slug': slug})


def create_superuser(phone='09380043744', password='test123456'):
    """create and return user """
    return get_user_model().objects.create_superuser(phone, password)

def get_token_for_user(user):
    """get token for user"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class PrivateApiTest(TestCase):
    """Test authenticated users API endpoints."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser()
        self.token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    def _create_product(self, **kwargs):
        defaults = {
            "title": "pro12",
            "slug": "pro12",
            "description": "this is pro12",
            "price": 12,
            "sku": "sku-pro12"
        }
        defaults.update(kwargs)
        product = Product.objects.create(**defaults, user=self.user)
        return product

    def test_create_product(self):
        """Test creating a new product."""
        payload = {
            "title": "pro12",
            "slug": "pro12",
            "description": "this is pro12",
            "price": 12,
            "sku": "sku-pro12"

        }
        res = self.client.post(PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.filter(slug=res.data['slug']).get()
        self.assertEqual(product.title, payload['title'])

    def test_retrieve_product(self):
        """Test retrieving a product."""
        product = self._create_product()
        res = self.client.get(detail_url(product.slug))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_product(self):
        """Test updating a product."""
        product = self._create_product()
        payload = {
            "title": "pro123",
            "slug": "pro123",
        }
        res = self.client.patch(detail_url(product.slug), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        product.refresh_from_db()
        self.assertEqual(product.title, payload['title'])
        self.assertEqual(product.price, 12)

    def test_update_product(self):
        """Test updating a product."""
        product = self._create_product()
        payload = {
            "title": "pro123",
            "slug": "pro123",
            "description": "this is pro123",
            "price": 12,
            "sku": '12e3de'
        }
        res = self.client.put(detail_url(product.slug), payload)
        product.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        for key, val in payload.items():
            self.assertEqual(getattr(product, key), val)

    def test_destroy_product(self):
        """Test deleting a product."""
        product = self._create_product()
        res = self.client.delete(detail_url(product.slug))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


