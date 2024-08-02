from datetime import datetime
from utils.basic_use_case import UseCase

from utils.response.paginate_response import PaginateResponse

from product.dto import GetProductsDTO
from product.models import Product, ProductRepository
from product.responses import ProductResponse


class DeleteProductUseCase(UseCase):
    
    def __init__(self) -> None:
        self.product_repository = ProductRepository()
        self.paginate_response = PaginateResponse()
        self.product_response = ProductResponse()

    def execute(self, product: Product) -> Product:
        product.is_active = False
        product.deleted_at = datetime.today()

        product.save()
        return product
