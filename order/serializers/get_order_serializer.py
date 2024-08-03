from rest_framework import serializers

from order.models import Order
from order.services import OrderValidators


class GetOrderSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    order = serializers.SerializerMethodField('_validate_order')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.order_validators = OrderValidators()

    def _validate_order(self, data: dict) -> Order:
        order_id = data.get('order_id')

        return self.order_validators.validate_order_exist_by_id(order_id)

