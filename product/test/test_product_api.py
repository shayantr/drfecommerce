"""
tests for product APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Product
from product.api.user import ProductSerializer

ADMIN_PRODUCT_URL = reverse('product:admin-products-list')
PRODUCT_URL = reverse('product:product-list')


def admin_detail_url(slug):
    """Return the url for product detail view"""
    return reverse('product:admin-products-detail', kwargs={'slug': slug})


def create_superuser(phone='09380043744', password='test123456'):
    """create and return user """
    return get_user_model().objects.create_superuser(phone, password)

def create_user(phone='09180043744', password='test123456'):
    """create and return user """
    return get_user_model().objects.create_user(phone, password)

def create_product(user, **kwargs):
    defaults = {
        "title": "pro12",
        "slug": "pro12",
        "description": "this is pro12",
        "price": 12,
        "sku": "sku-pro12"
    }
    defaults.update(kwargs)
    product = Product.objects.create(**defaults, user=user)
    return product


def get_token_for_user(user):
    """get token for user"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class PublicApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_product_list(self):
        user = create_user()
        p1 = create_product(user=user)
        p2_detail = {
            "title": "pro11122",
            "slug": "pro11212",
            "description": "1th12is is pro12",
            "price": 12112,
            "sku": "sku-p1r12o12"
        }
        p2 = create_product(user=user, **p2_detail)
        res = self.client.get(PRODUCT_URL)
        s1 = ProductSerializer(p1)
        s2 = ProductSerializer(p2)
        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class PrivateAdminApiTest(TestCase):
    """Test authenticated users API endpoints."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser()
        self.token = get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')


    def test_create_product(self):
        """Test creating a new product."""
        payload = {
            "title": "pro12",
            "slug": "pro12",
            "description": "this is pro12",
            "price": 12,
            "sku": "sku-pro12"

        }
        res = self.client.post(ADMIN_PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.filter(slug=res.data['slug']).get()
        self.assertEqual(product.title, payload['title'])

    def test_retrieve_product(self):
        """Test retrieving a product."""
        product = create_product(user=self.user)
        res = self.client.get(admin_detail_url(product.slug))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patch_product(self):
        """Test updating a product."""
        product = create_product(user=self.user)
        payload = {
            "title": "pro123",
            "slug": "pro123",
        }
        res = self.client.patch(admin_detail_url(product.slug), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        product.refresh_from_db()
        self.assertEqual(product.title, payload['title'])
        self.assertEqual(product.price, 12)

    def test_update_product(self):
        """Test updating a product."""
        product = create_product(user=self.user)
        payload = {
            "title": "pro123",
            "slug": "pro123",
            "description": "this is pro123",
            "price": 12,
            "sku": '12e3de'
        }
        res = self.client.put(admin_detail_url(product.slug), payload)
        product.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        for key, val in payload.items():
            self.assertEqual(getattr(product, key), val)

    def test_destroy_product(self):
        """Test deleting a product."""
        product = create_product(user=self.user)
        res = self.client.delete(admin_detail_url(product.slug))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


