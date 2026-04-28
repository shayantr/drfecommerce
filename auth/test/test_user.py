from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

SIGN_IN_URL = reverse("auth:login")
REGISTER_URL = reverse("auth:register")


def create_user(phone="09380043744", password="password@123ASD"):
    user = get_user_model().objects.create_user(phone=phone, password=password)
    return user


class PrivateUserApiTest(TestCase):
    def setUp(self):
        client = APIClient()

    def test_sign_in(self):
        user = create_user()
        payload = {
            'phone': '09380043744',
            'password': 'password@123ASD'
        }
        res = self.client.post(SIGN_IN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user'], user.phone)

    def test_register(self):
        payload = {
            'phone': '09380043744',
            'password': 'password@123ASD',
            'password_2': 'password@123ASD',
        }
        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
