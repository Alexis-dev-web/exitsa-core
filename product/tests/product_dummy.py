from django.core.paginator import Paginator

from product.models import Product
from user.models import User


class ProductDummy:

    def build_user_test(self, email='testing@exitosa.test'):
        user = User()
        user.first_name = 'test'
        user.last_name = 'tets last name'
        user.email = email
        user.is_superuser = True

        return user

    def build_product_test(self):
        product = Product()
        product.sku = 'NEW2023'
        product.name = 'product 2023'
        product.description = 'New product'
        product.type = 'PHYSIC'
        product.state = 'IN_STOCK'
        product.base_cost = 255.00
        product.base_pricing = 500
        product.in_existence = 25

        return product

    def build_paginator_products(self, limit: int = 10):
        product = self.build_product_test()
        product_two = self.build_product_test()
        product_two.sku = 'NE2021'
        product_three = self.build_product_test()
        product_three.sku = 'NE021'

        products = [
            product,
            product_two,
            product_three
        ]

        return Paginator(products, limit)


    def build_dict_product(self):
        return {
            "sku": "PO11",
            "name": "Llave allen",
            "description": "Herramienta",
            "type": "PHYSIC",
            "state": "IN_STOCK",
            "base_pricing": 250.5,
            "base_cost": 150.0,
            "in_existence": 85
        }