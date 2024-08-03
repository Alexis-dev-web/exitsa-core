from dataclasses import dataclass
from utils.base_dto import BaseDto


@dataclass
class PaginateBaseDTO(BaseDto):
    page: int = 1
    limit: int = 10
