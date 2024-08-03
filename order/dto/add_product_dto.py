from dataclasses import dataclass
from utils.base_dto import BaseDto

from order.models import Order
from product.models import Product


@dataclass
class AddProductDTO(BaseDto):
    product_id: str
    quantity: int
    product: Product
    price: float = None
    order: Order = None
