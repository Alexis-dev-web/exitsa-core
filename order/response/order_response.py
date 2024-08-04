from order.models import Order
from .order_products_response import OrderProductResponse


class OrderResponse:

    def __init__(self) -> None:
        self.order_product_response = OrderProductResponse()

    def to_json(self, order: Order) -> dict:
        return {
            'id': str(order.id),
            'code': order.code,
            'number': order.number,
            'total_price': order.total_price,
            'status': order.status,
            'type': order.type,
            'is_active': order.is_active,
            'is_paid': order.is_paid,
            'real_delivered_date': str(order.real_delivered_date),
            'paid_date': str(order.paid_date),
            'delivered_date': str(order.delivered_date),
            'reason_cancelled': order.reason_cancelled,
            'client_id': str(order.client.id) if order.client else None,
            'store': str(order.store.id) if order.store else None,
            'created_at': str(order.created_at),
            'updated_at': str(order.updated_at)
        }

    def response_with_products(self, order: Order, products: list) -> dict: 
        response = self.to_json(order)
        response['products'] = [self.order_product_response.response_with_product_data(product) for product in products or []]

        return response

    def create_report(self, orders_by_status, product_more_sale) -> dict:
        response = {
            'orders_group': orders_by_status,
            'product_more_sale': product_more_sale
        }
        
        return response
