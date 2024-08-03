from rest_framework import serializers

from utils.error_messages import messages
from product.models import Product
from product.serializers import CreateProductSerializer


class UpdateProductSerializer(CreateProductSerializer):
    is_sould_out = serializers.BooleanField(required=False)
    product_id = serializers.UUIDField()
    product = serializers.SerializerMethodField('_validate_product')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

    def _validate_product(self, data: dict) -> Product:
        sku = data.get('sku', None)
        product_id = data.get('product_id', None)

        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise serializers.ValidationError({'product': messages['product_not_exist']})

        product_exist = self.product_repository.get_by_sku(sku)

        if product_exist and product_exist.id != product.id:
            raise serializers.ValidationError({'sku': messages['product_sku_exists']}) 

        return product

    def validate(self, data: dict) -> dict:
        return data
