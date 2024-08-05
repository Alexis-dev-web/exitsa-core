from rest_framework import serializers

from utils.error_messages import messages
from store.models import Store
from product.models import Product, ProductRepository
from .add_alert_product_serializer import AddAlertProductSerializer


class CreateProductSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    image_preview = serializers.CharField(required=False)
    type = serializers.ChoiceField(Store.STORE_CHOICE)
    state = serializers.ChoiceField(Product.STATE_PRODUCT_CHOICE)
    base_pricing = serializers.FloatField()
    base_cost = serializers.FloatField(required=False)
    in_existence = serializers.IntegerField()
    alert = AddAlertProductSerializer(required=False)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.product_repository = ProductRepository()

    def validate(self, data: dict) -> dict:
        sku = data.get('sku', None)

        product = self.product_repository.get_by_sku(sku)
        if product:
            raise serializers.ValidationError({'sku': messages['product_sku_exists']}) 

        return data
