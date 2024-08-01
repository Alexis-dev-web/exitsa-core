import uuid

from django.db import models


class Store(models.Model):
    STORE_CHOICE = [
        ('PHYSIC', 'PHYSIC'),
        ('DIGITAL', 'DIGITAL'),
        ('BOTH', 'BOTH')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000, null=True)
    url = models.CharField(max_length=255, null=True)
    type = models.CharField(choices=STORE_CHOICE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

