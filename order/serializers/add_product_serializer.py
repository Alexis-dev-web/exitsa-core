from rest_framework import serializers

from product.services import ProductValidators
from product.models import Product


class AddProductSerializer(serializers.Serializer):
    price = serializers.FloatField(required=False)
    quantity = serializers.IntegerField()
    product_id = serializers.UUIDField()
    product = serializers.SerializerMethodField('_validate_product')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.product_validator = ProductValidators()

    def _validate_product(self, data: dict) -> Product:
        product_id = data.get('product_id', None)

        return self.product_validator.validate_product_exist_by_id(product_id)

