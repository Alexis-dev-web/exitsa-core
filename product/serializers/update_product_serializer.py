from rest_framework import serializers

from utils.error_messages import messages
from store.models import Store
from product.models import Product, ProductRepository


class UpdateProductSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    image_preview = serializers.CharField(required=False)
    type = serializers.ChoiceField(Store.STORE_CHOICE)
    state = serializers.ChoiceField(Product.STATE_PRODUCT_CHOICE)
    base_pricing = serializers.FloatField()
    base_cost = serializers.FloatField(required=False)
    in_existence = serializers.IntegerField()
    is_sould_out = serializers.BooleanField(required=False)
    product_id = serializers.UUIDField()
    product = serializers.SerializerMethodField('_validate_product')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.product_repository = ProductRepository()

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