from rest_framework import serializers

from utils.error_messages import messages
from order.models import Order
from order.services import OrderValidators
from order.serializers import OrderSerializer


class UpdateOrderSerializer(OrderSerializer):
    order_id = serializers.UUIDField()    
    order = serializers.SerializerMethodField('_validate_order')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.order_validators = OrderValidators()

    def _validate_order(self, data: dict) -> Order:
        order_id = data.get('order_id')

        return self.order_validators.validate_order_exist_by_id(order_id)

    def validate(self, data: dict) -> dict:
        is_paid = data.get('is_paid')
        date_paid = data.get('date_paid', False)

        if is_paid and not date_paid:
            raise serializers.ValidationError({'date_paid': [messages['date_paid_required']]})

        return data
