from datetime import datetime
from utils.basic_use_case import UseCase

from order.models import Order
from order.response import OrderResponse
from order.dto import UpdateOrderStateDTO
from product.use_case import UpdateInventoryProductUseCase
from order.response import OrderResponse

class UpdateOrderStateUseCase(UseCase):

    def __init__(self) -> None:
        self.order_response = OrderResponse()
        self.update_inventory_product_use_case = UpdateInventoryProductUseCase()

    def execute(self, request: UpdateOrderStateDTO) -> Order:
        sent_products = False
        order = request.order
        order.reason_cancelled = request.reason_cancel

        if order.status == 'NOT_COMPLETED':
            products = order.products.filter(sent=True)
        else:
            products = order.products.all()

        if request.state == 'SENT':
            order.delivered_date = request.delivered_date if request.delivered_date else datetime.today()
            sent_products = True

        if not sent_products:
            if (order.status == 'SENT' and request.state == 'CANCELLED' ) or (order.status == 'DELIVERED' and request.state == 'REJECTED'):
                sent_products = True

        if sent_products:
            for product in products:
                sent, next_date_to_sent = self.update_inventory_product_use_case.execute(product.product, order.type, product.quantity, request.state)

                if sent and order.status == 'SENT':
                    product.sent = True
                    product.next_available = next_date_to_sent
                    product.save()

                if not sent and request.state == 'SENT':
                    request.state = 'NOT_COMPLETED'

                    if not request.wait_missing_products:
                        order.total_price -= product.price
                        product.delete()

        order.status = request.state
        order.save()
        


        return order