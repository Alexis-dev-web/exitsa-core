from rest_framework import serializers

from store.models import Store, StoreHasProduct
from store.services import StoreValidators
from product.services import ProductValidators
from product.models import Product


class AddProductToSoreSerializer(serializers.Serializer):
    current_price = serializers.FloatField(required=False)
    is_sould_out = serializers.BooleanField(required=False)
    store_id = serializers.UUIDField()
    product_id = serializers.UUIDField()
    store = serializers.SerializerMethodField('_validate_store')
    product = serializers.SerializerMethodField('_validate_product')
    store_product = serializers.SerializerMethodField('_validate_exist')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.store_validator = StoreValidators()
        self.product_validator = ProductValidators()

    def _validate_store(self, data: dict) -> Store:
        store_id = data.get('store_id', None)

        return self.store_validator.validate_store(store_id)

    def _validate_product(self, data: dict) -> Product:
        product_id = data.get('product_id', None)

        return self.product_validator.validate_product_exist_by_id(product_id)

    def _validate_exist(self, data: dict) -> StoreHasProduct:
        store_id = data.get('store_id', None)
        product_id = data.get('product_id', None)
        
        return self.store_validator.validate_exist_product_in_store(store_id, product_id)

