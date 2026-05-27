import requests
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import APIException

from app import settings
from app.settings import START_PAY_URL, CALL_BACK_URL, MERCHANT_ID, PAYMENT_URL, VERIFY_URL


class ZarinGatWay:
    def _start_pay_url(self, authority):
        return f"{START_PAY_URL}{authority}"

    def _call_back_url(self, reverse_url):
        return f"{CALL_BACK_URL}{reverse_url}"

    def __init__(self, user_order):
        self.user_order = user_order

    def request(self):
        payload = {
            'merchant_id': MERCHANT_ID,
            'amount': self.user_order.final_amount,
            'callback_url': self._call_back_url(reverse('purchase:payment-call-back')),
            "description": "Transaction description.",
            'metadata': {
                'order_id': str(self.user_order.id),
                'mobile': str(self.user_order.user.phone),
            }

        }
        try:
            response = requests.post(PAYMENT_URL, json=payload, timeout=10)
            result = response.json()
        except requests.Timeout:
            return {
                'success': False,
                'error': "Gateway timed out.",
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
        try:
            return self._start_pay_url(authority)
        except APIException as e:
            return {
                "success": False,
                "error": str(e),
            }



    def verify(self, authority):
        payload = {
            "merchant_id": MERCHANT_ID,
            "amount": self.user_order.final_amount,
            "authority": authority,
        }
        try:
            res = requests.post(VERIFY_URL, json=payload, timeout=10)
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
