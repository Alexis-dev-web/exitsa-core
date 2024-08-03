from utils.basic_use_case import UseCase

from order.dto import CreateOrderDTO
from order.response import OrderResponse


class UpdateOrderUseCase(UseCase):

    def __init__(self) -> None:
        super().__init__()
        self.order_response = OrderResponse()

    def execute(self, request: CreateOrderDTO) -> dict:
        order = request.order
        order.type = request.type
        order.status = request.status
        order.client = request.client
        order.store = request.store
        order.total_price = request.total_price
        order.is_paid = request.is_paid

        if request.is_paid:
            order.paid_date = request.date_pay

        order.save()

        products = [self.add_product_oder_use_case.execute(product, order) for product in request.products or []] 

        return self.order_response.response_with_products(order, products)

