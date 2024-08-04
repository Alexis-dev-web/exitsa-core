from datetime import datetime, timedelta, date
from utils.basic_use_case import UseCase

from order.models import OrderRepository, OrderProductsRepository
from order.response import OrderResponse
from order.dto import GetOrdersReportDTO


class OrderReportsUseCase(UseCase):

    def __init__(self) -> None:
        self.order_response = OrderResponse()
        self.order_repository = OrderRepository()
        self.order_products_repository = OrderProductsRepository()

    def execute(self, request: GetOrdersReportDTO) -> dict:
        if not request.start_date:
            request.end_date = date.today()
            request.start_date = request.end_date - timedelta(weeks=4)

        start_date = datetime.strptime(str(request.start_date), '%Y-%m-%d')
        print('pp')
        end_date = datetime.strptime(str(request.end_date), '%Y-%m-%d')

        orders_group = self.order_repository.get_all_group_by_status(start_date, end_date)
        product_more_sale = self.order_products_repository.get_more_sale(start_date, end_date)

        return self.order_response.create_report(
            orders_by_status=orders_group,
            product_more_sale=product_more_sale
        )
