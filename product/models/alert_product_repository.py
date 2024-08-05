from django.core.paginator import Paginator

from .alert_product import AlertProduct


class AlertProductRepository:

    def get_by_id(self, id: str) -> AlertProduct:
        return AlertProduct.objects.filter(id=id).first()

    def get_all(self) -> list[AlertProduct]:
        return AlertProduct.objects.all()

    def get_default(self) -> AlertProduct:
        return AlertProduct.objects.filter(is_active=True, is_default=True).first()

    def get_paginate(self, limit: int) -> Paginator:
        stores = AlertProduct.objects.all()
        paginator = Paginator(stores, limit)
        
        return paginator

    def get_by_product(self, product_id: str) -> AlertProduct:
        return AlertProduct.objects.filter(is_active=True, product__id=product_id).first()

