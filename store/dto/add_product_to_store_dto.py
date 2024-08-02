from dataclasses import dataclass
from utils.base_dto import BaseDto

from store.models import Store
from product.models import Product


@dataclass
class AddProductToStoreDTO(BaseDto):
    product_id: str
    store_id: str
    store: Store
    product: Product
    is_sould_out: bool = False
    current_price: float = None

