from dataclasses import dataclass

from utils.base_dto import BaseDto
from product.models import Product


@dataclass
class CreateOrUpdateDTO(BaseDto):
    name: str
    description: str
    sku: str
    type: str
    base_pricing: float
    in_existence: int
    is_active: bool = True
    state: str = 'IN_STOCK'
    base_cost: float = None
    image_preview: str = None
    product_id: str = None
    product: Product = None

