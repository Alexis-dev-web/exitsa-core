from django.core.paginator import Paginator
from .order import Order


class OrderRepository:

    def get_by_id(self, id: str) -> Order:
        return Order.objects.filter(id=id).first()

    def get_last_register_by_type(self, type: str) -> Order:
        try:
            return Order.objects.filter(type=type).latest('created_at')
        except:
            return None

    def get_all(self) -> list[Order]:
        return Order.objects.all()

    def get_by_dynamic_filters_paginate(self, filters: dict, limit: int = 10) -> Paginator:
        orders = Order.objects.filter(**filters).order_by('-created_at')
        paginator = Paginator(orders, limit)
        return paginator

    def get_all_paginate(self, limit: int = 10) -> Paginator:
        orders = Order.objects.all().order_by('-created_at')
        paginator = Paginator(orders, limit)
        return paginator
