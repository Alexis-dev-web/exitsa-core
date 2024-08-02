from utils.basic_use_case import UseCase

from product.dto import CreateOrUpdateDTO
from product.models import Product, ProductRepository


class CreateOrUpdateProductUseCase(UseCase):
    
    def __init__(self) -> None:
        self.product_repository = ProductRepository()

    def execute(self, request: CreateOrUpdateDTO):
        product = Product() if not request.product else request.product
        product.name = request.name
        product.sku = request.sku.upper()
        product.description = request.description
        product.type = request.type
        product.base_cost = request.base_cost
        product.base_pricing = request.base_pricing
        product.state = request.state
        product.in_existence = request.in_existence

        product.save()
        return product
