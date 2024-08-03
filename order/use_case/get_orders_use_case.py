from utils.basic_use_case import UseCase
from datetime import datetime

from .add_product_to_order_use_case import AddProductToOrderUseCase

from order.dto import GetOrdersDTO
from order.models import OrderRepository
from order.response import OrderResponse
from utils.response.paginate_response import PaginateResponse


class GetOrdersUseCase(UseCase):

    def __init__(self) -> None:
        self.add_product_oder_use_case = AddProductToOrderUseCase()
        self.order_response = OrderResponse()
        self.order_repository = OrderRepository()
        self.paginate_response = PaginateResponse()

    def execute(self, request: GetOrdersDTO) -> dict:
        if not request.status and not request.start_date and not request.type and not request.min_price and not request.max_price:
            orders = self.order_repository.get_all_paginate(request.limit)
        else:
            filters = {}
            if request.status:
                filters['status'] = request.status
            if request.type:
                filters['type'] = request.type
            if request.min_price:
                filters['total_price__gte'] = request.min_price
            if request.max_price:
                filters['total_price__lte'] = request.max_price

            if request.start_date:
                start_date = datetime.strptime(request.start_date, '%Y-%m-%d')

                if not request.end_date:
                    request.end_date = str(datetime.today())

                end_date = datetime.strptime(request.end_date, '%Y-%m-%d')
                filters['created_at__range'] = (start_date, end_date)

            orders = self.order_repository.get_by_dynamic_filters_paginate(filters, request.limit)

        page = orders.page(request.page)
        items = [self.order_response.to_json(order) for order in page.object_list or []]

        return self.paginate_response.to_json(page, orders.num_pages, orders.count, items)

