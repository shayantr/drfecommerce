import requests
from django.urls import reverse
from rest_framework import serializers

from app import settings


class ZarinGatWay:
    MERCHANT_ID = settings.MERCHANT_ID
    PAYMENT_URL = settings.PAYMENT_URL
    VERIFY_URL = settings.VERIFY_URL
    CALL_BACK_URL = settings.CALL_BACK_URL
    START_PAY_URL = settings.START_PAY_URL
    def _start_pay_url(self, authority):
        return f"{self.START_PAY_URL}{authority}"

    def _call_back_url(self, reverse_url):
        return f"{self.CALL_BACK_URL}{reverse_url}"

    def __init__(self, order):
        self.order = order

    def request(self):

        payload = {
            'merchant_id': self.MERCHANT_ID,
            'amount': self.order.total_amount,
            'callback_url': self._call_back_url(reverse('purchase:payment-call-back')),
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
            return self._start_pay_url(authority)
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
