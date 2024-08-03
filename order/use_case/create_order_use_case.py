from utils.basic_use_case import UseCase

from .add_product_to_order_use_case import AddProductToOrderUseCase

from order.models import Order, OrderRepository
from order.dto import CreateOrderDTO
from order.response import OrderResponse



class CreateOrderUseCase(UseCase):

    def __init__(self) -> None:
        super().__init__()
        self.add_product_oder_use_case = AddProductToOrderUseCase()
        self.order_response = OrderResponse()
        self.order_repository = OrderRepository()

    def execute(self, request: CreateOrderDTO) -> dict:
        code = 'EXBY00' if not request.type == 'SALE' else 'EXSL00'
        last_order = self.order_repository.get_last_register_by_type(request.type)

        order = Order()
        order.type = request.type
        order.number = last_order.number + 1 if last_order else 1
        order.status = request.status
        # order.seller = request.seller
        order.client = request.client
        order.store = request.store
        order.total_price = request.total_price
        order.is_paid = request.is_paid

        if request.is_paid:
            order.paid_date = request.date_pay

        if last_order:
            code = f'{code}{str(last_order.number)}'
        else:
            code = f'{code}1'

        order.code = code
        order.save()

        products = [self.add_product_oder_use_case.execute(product, order) for product in request.products or []] 

        return self.order_response.response_with_products(order, products)

