from django.core.paginator import Paginator

from .product import Product


class ProductRepository:

    def get_by_id(self, id: str) -> Product:
        return Product.objects.filter(id=id).first()

    def get_all(self) -> list[Product]:
        return Product.objects.all()

    def get_by_sku(self, sku: str) -> Product:
        return Product.objects.filter(sku=sku).first()

    def get_paginate(self, limit: int) -> Paginator:
        stores = Product.objects.all()
        paginator = Paginator(stores, limit)
        
        return paginator
