from dataclasses import dataclass

from utils.base_dto import BaseDto


@dataclass
class GetProductsDTO(BaseDto):
    page: int = 1
    limit: int = 10
