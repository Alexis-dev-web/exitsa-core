from dataclasses import dataclass
from utils.base_dto import BaseDto


@dataclass
class GetUsersDTO(BaseDto):
    email: str = None
    gender: str = None
    page: int = 1
    limit: int = 10
