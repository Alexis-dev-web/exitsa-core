from rest_framework import serializers

from utils.error_messages import messages
from order.models import Order
from order.services import OrderValidators


class UpdateOrderStateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(Order.STATUS_CHOICE)
    wait_missing_products = serializers.BooleanField(required=False)
    reason_cancel = serializers.CharField(max_length=1000, required=False)
    order_id = serializers.UUIDField()
    order = serializers.SerializerMethodField('_validate_order')
    delivered_date = serializers.DateField(required=False)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.order_validators = OrderValidators()

    def _validate_order(self, data: dict) -> Order:
        order_id = data.get('order_id')
        state = data.get('state')

        order = self.order_validators.validate_order_exist_by_id(order_id)

        return order

    def validate(self, data: dict) -> dict:
        state = data.get('state')

        if state == 'CANCELLED' or state == 'REJECTED':
            reason_cancel = data.get('reason_cancel', None)
            if not reason_cancel:
                raise serializers.ValidationError({'reason_cancelled': [messages['reason_cancel_required']]})

        return data