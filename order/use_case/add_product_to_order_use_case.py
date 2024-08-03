from utils.basic_use_case import UseCase

from order.models import OrderProduct, Order
from order.dto import AddProductDTO


class AddProductToOrderUseCase(UseCase):
    
    def execute(self, product: AddProductDTO, order: Order) -> OrderProduct:
        order_product = OrderProduct()
        order_product.price = product.price if product.price else product.product.base_pricing
        order_product.product = product.product
        order_product.order = order
        order_product.quantity = product.quantity

        order_product.save()

        return order_product
