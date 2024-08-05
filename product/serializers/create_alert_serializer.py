from rest_framework import serializers

from product.models import Product
from product.services import ProductValidators
from .add_alert_product_serializer import AddAlertProductSerializer


class CreateAlertProductSerializer(AddAlertProductSerializer):
    min_quantity = serializers.IntegerField()
    is_default = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    product_id = serializers.UUIDField()
    product = serializers.SerializerMethodField('_validate_product')
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.product_validators = ProductValidators()
        
    def _validate_product(self, data: dict):
        product_id = data.get('product_id', None)

        product = self.product_validators.validate_product_exist_by_id(product_id)

        return product

