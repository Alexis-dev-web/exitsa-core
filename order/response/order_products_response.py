from utils.base_response import BaseResponseModel

from order.models import OrderProduct
from product.responses import ProductResponse


class OrderProductResponse:

    def __init__(self) -> None:
        self.product_response = ProductResponse()

    def to_json(self, order_product: OrderProduct) -> dict:
        return {
            'id': str(order_product.id),
            'quantity': order_product.quantity,
            'sent': order_product.sent,
            'next_available': str(order_product.next_available),
            'price': order_product.price,
            'order_id': str(order_product.order.id),
            'product_id': str(order_product.product.id),
            'created_at': str(order_product.created_at),
            'updated_at': str(order_product.updated_at)
        }

    def response_with_product_data(self, order_product: OrderProduct) -> dict:
        response = self.to_json(order_product)
        response['product'] = self.product_response.to_json(order_product.product)

        return response
