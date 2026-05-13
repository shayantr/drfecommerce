"""
Test invoice APIs
Note that set CELERY_TASK_ALWAYS_EAGER = True and CELERY_TASK_EAGER_PROPAGATES = True
for celery testing
"""

from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Product, Cart, UserCart, UserAddress, UserOrder, Order, Payment
from core.models.order import OrderStatus
from purchase.api.user.order import UserOrderDetailSerializer
from purchase.tasks import check_order_status

URL = reverse('purchase:order-list')
def detail_url(order_id):
    return reverse('purchase:order-detail', args=[order_id])
def create_user(phone='09380043744', password='password@1234123rDFD'):
    return get_user_model().objects.create(phone=phone, password=password)

def create_product(user, **kwargs):
    payload = {
        "user": user,
        "title": "pro1234242",
        "slug": "slug-product",
        "description": "this is pro12",
        "price": 125000,
        "quantity": 5,
        "sku": "sku-pro122323"
    }
    payload.update(kwargs)
    return Product.objects.create(**payload)

def createAddress(user, **kwargs):
    payload = {
        'user': user,
        'name': 'shayan',
        'last_name': 'tora',
        'street': '1234',
        'city': 'tehran',
        'post_code': 'ca',
        'province': 'tehran',
        'details': 'detail'
    }
    payload.update(kwargs)
    return UserAddress.objects.create(**payload)

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class PrivateInvoiceApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(get_token(self.user)))
        self.product = create_product(user=self.user)
        self.address = createAddress(user=self.user)
        self.user_cart = UserCart.objects.create(user=self.user)
        self.cart = Cart.objects.create(cart=self.user_cart, product=self.product, quantity=2)
    def test_add_to_invoice(self):
        payload = {
            'address': self.address.id,
        }
        res = self.client.post(URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Cart.objects.filter(id=self.cart.id).exists())
        self.assertFalse(UserCart.objects.filter(id=self.user_cart.id).exists())

    def test_get_invoice(self):
        user_order = UserOrder.objects.create(user=self.user, address=self.address)
        order = Order.objects.create(
            order=user_order,
            product=self.product,
            price=self.product.price,
            quantity=2
        )
        url = detail_url(user_order.id)
        res = self.client.get(url)
        s1 = UserOrderDetailSerializer(user_order)
        self.assertEqual(s1.data, res.data)

    def test_celery_order_paid(self):
        user_order = UserOrder.objects.create(user=self.user, address=self.address)
        order = Order.objects.create(
            order=user_order,
            product=self.product,
            price=self.product.price,
            quantity=2
        )
        payment = Payment.objects.create(
            user=self.user,
            order=user_order,
            amount=1,
            status=2,
            ip_address='1.1.1.1',
            transaction_id='transaction_id',
            gateway='1.1.1.1',
        )
        check_order_status.delay(user_order.id)
        user_order.refresh_from_db()
        self.assertEqual(user_order.status, OrderStatus.PENDING)
