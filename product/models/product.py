import uuid

from django.db import models
from store.models import Store


class Product(models.Model):
    STATE_PRODUCT_CHOICE = [
        ('IN_STOCK', 'IN_STOCK'),
        ('REFILLING', 'REFILLING'),
        ('SOULD_OUT', 'SOULD_OUT')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image_preview = models.CharField(max_length=255, null=True)
    type = models.CharField(choices=Store.STORE_CHOICE)
    state = models.CharField(choices=STATE_PRODUCT_CHOICE)
    base_pricing = models.FloatField(default=0.0)
    base_cost = models.FloatField(null=True)
    in_existence = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

