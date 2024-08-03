import uuid

from django.db import models
from store.models import Store
from user.models import User


class Order(models.Model):
    TYPE_CHOICE = [
        ('SALE', 'SALE'),
        ('BUY', 'BUY')
    ]

    STATUS_CHOICE = [
        ('CREATE', 'CREATE'),
        ('CANCELLED', 'CANCELLED'),
        ('SENT', 'SENT'),
        ('DELIVERED', 'DELIVERED'),
        ('REJECTED', 'REJECTED'),
        ('NOT_COMPLETED', 'NOT_COMPLETED')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100)
    number = models.IntegerField()
    total_price = models.FloatField(default=0.0)
    status = models.CharField(choices=STATUS_CHOICE, default='CREATE')
    type = models.CharField(choices=TYPE_CHOICE, default='SALE')
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True)
    delivered_date = models.DateField(null=True)
    real_delivered_date = models.DateField(null=True)
    reason_cancelled = models.CharField(max_length=1000, null=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

