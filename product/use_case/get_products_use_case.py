from utils.basic_use_case import UseCase

from utils.response.paginate_response import PaginateResponse

from product.dto import GetProductsDTO
from product.models import ProductRepository
from product.responses import ProductResponse


class GetProductsUseCase(UseCase):
    
    def __init__(self) -> None:
        self.product_repository = ProductRepository()
        self.paginate_response = PaginateResponse()
        self.product_response = ProductResponse()

    def execute(self, request: GetProductsDTO):
        products = self.product_repository.get_paginate(request.limit)

        page = products.page(request.page)

        items = [self.product_response.to_json(product) for product in page.object_list or []]

        return self.paginate_response.to_json(page, products.num_pages, products.count, items)
