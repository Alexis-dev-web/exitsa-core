from rest_framework import serializers

from utils.error_messages import messages
from order.models import Order, OrderRepository

class OrderValidators:

    def __init__(self) -> None:
        self.order_repository = OrderRepository()

    def validate_order_exist_by_id(self, id: str) -> Order:
        order = self.order_repository.get_by_id(id)

        if not order:
            raise serializers.ValidationError({'store': messages['order_not_exist']})

        return order
