from typing import List
from datetime import date
from dataclasses import dataclass, field
from utils.base_dto import BaseDto

from .add_product_dto import AddProductDTO
from user.models import User
from store.models import Store
from order.models import Order


@dataclass
class CreateOrderDTO(BaseDto):
    is_paid: bool
    type: str
    client_id: str = None
    delivered_date: date = None
    date_pay: date = field(default_factory=date.today)
    store_id: str =  None
    products: List[AddProductDTO] = field(default_factory=list)
    status: str = 'CREATE'
    total_price: float = None
    store: Store = None
    client: User = None
    order: Order = None

    def __post_init__(self):
        self.products = [AddProductDTO.from_json(product) for product in self.products or []]

