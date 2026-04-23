import tempfile
from unittest import TestCase

from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import Token, RefreshToken

from core.models import User, ProductImage

UPLOAD_IMAGE = reverse('product:upload-image')
def create_superuser(phone='09380043744', password="123456778"):
    return get_user_model().objects.create_superuser(phone=phone, password=password)

def get_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class ImageProductTestCase(TestCase):
    def setUp(self):
        self.user = create_superuser()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_jwt_token(self.user))

    def test_upload_image(self):
        """Test uploading image"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as fp:
            img = Image.new('RGB', size=(100, 100))
            img.save(fp)
            fp.seek(0)
            payload = {
                'image': fp,
                "user": self.user.id,
            }
            res = self.client.post(UPLOAD_IMAGE, payload, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
