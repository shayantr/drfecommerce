import requests
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ZarinGatWay:
    MERCHANT_ID = "2549e168-d901-231c-812b-716adbdbef83"
    PAYMENT_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"

    def _call_back_url(self):
        return f"localhost:8000{reverse('orders:payment-call-back')}"

    def __init__(self, order):
        self.order = order

    def request(self):

        payload = {
            'merchant_id': self.MERCHANT_ID,
            'amount': self.order.total_amount,
            'callback_url': self._call_back_url(),
            "description": "Transaction description.",
            'metadata': {
                'order_id': str(self.order.id),
                'mobile': str(self.order.user.phone),
            }

        }
        res = requests.post(self.PAYMENT_URL, json=payload)
        data = res.json()
        if data['data']['code'] == 100:
            return data['data']
        else:
            return data['errors']

    def get_link(self, authority):
        if authority:
            return f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"
        else:
            return serializers.ValidationError('error on request')

    def verify(self, authority, status, payment):
        payload = {
            "merchant_id": self.MERCHANT_ID,
            "amount": self.order.total_amount,
            "authority": authority,
        }
        res = requests.post(self.VERIFY_URL, json=payload)
        result = res.json()
        if result['data']['code'] == 100 or 101:
            status = 2
        else:
            status = 3
        return status

    def __str__(self):
        return "ZarinGatWay"

    def __repr__(self):
        return "ZarinGatWay"
