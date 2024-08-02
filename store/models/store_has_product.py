import uuid

from django.db import models
from .store import Store
from product.models import Product


class StoreHasProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_price = models.FloatField(default=0.0)
    is_sould_out = models.BooleanField(default=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


