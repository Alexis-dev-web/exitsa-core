from rest_framework import serializers

from product.models import Product
from product.services import ProductValidators


class AddAlertProductSerializer(serializers.Serializer):
    min_quantity = serializers.IntegerField()

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.product_validators = ProductValidators()
