from dataclasses import dataclass
from datetime import date
from utils.base_dto import BaseDto


@dataclass
class GetOrdersDTO(BaseDto):
    start_date: date = None
    end_date: date = None
    status: str = None
    type: str = None
    min_price: float = None
    max_price: float = None
    page: int = 1
    limit: int = 10
