import requests
from django.urls import reverse
from rest_framework import serializers


class ZarinGatWay:
    MERCHANT_ID = "2549e168-d901-231c-812b-716adbdbef83"
    PAYMENT_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"

    def _call_back_url(self):
        return f"https://localhost:8000{reverse('purchase:payment-call-back')}"

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
        try:
            response = requests.post(self.PAYMENT_URL, json=payload, timeout=10)
            result = response.json()
        except requests.Timeout:
            return {
                'success': False,
                'error': "Gateway timed out.",
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
            }
        if result.get("errors"):
            return {
                "success": False,
                "error": result["errors"],
            }
        return {
            "success": True,
            "data": result['data'],
        }

    def get_link(self, authority):
        if authority:
            return f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"
        else:
            return serializers.ValidationError('error on request')


    def verify(self, authority):
        payload = {
            "merchant_id": self.MERCHANT_ID,
            "amount": self.order.total_amount,
            "authority": authority,
        }
        try:
            res = requests.post(self.VERIFY_URL, json=payload, timeout=10)
            result = res.json()
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e),
            }
        if result.get("errors"):
            return {
                "success": False,
                "error": result["errors"],
            }
        code = result['data']['code']
        if code in [100, 101]:
            return {
                "success": True,
                "data": result['data'],
            }
        else:
            return {
                "success": False,
                "error": result['errors'],
            }


    def __str__(self):
        return "ZarinGatWay"

    def __repr__(self):
        return "ZarinGatWay"
