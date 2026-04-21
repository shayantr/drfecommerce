import uuid

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
    id = models.BigAutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)