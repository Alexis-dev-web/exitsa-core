from dataclasses import dataclass
from datetime import date

from utils.base_dto import BaseDto

from order.models import Order


@dataclass
class UpdateOrderStateDTO(BaseDto):
    state: str
    order_id: str
    wait_missing_products: bool = True
    order: Order = None
    reason_cancel: str = None
    delivered_date: date = None
