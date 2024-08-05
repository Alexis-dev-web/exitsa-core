from dataclasses import dataclass

from utils.base_dto import BaseDto
from product.models import Product


@dataclass
class AlertProductDTO(BaseDto):
    min_quantity: int
    is_active: bool = True
    is_default: bool = False
    product_id: str = None
    product: Product = None
