from utils.basic_use_case import UseCase

from .add_product_to_order_use_case import AddProductToOrderUseCase

from order.models import Order, OrderRepository
from order.response import OrderResponse


class GetOrderUseCase(UseCase):

    def __init__(self) -> None:
        super().__init__()
        self.add_product_oder_use_case = AddProductToOrderUseCase()
        self.order_response = OrderResponse()
        self.order_repository = OrderRepository()

    def execute(self, request: Order) -> dict:
        products = request.products.all()

        return self.order_response.response_with_products(request, products)
       

