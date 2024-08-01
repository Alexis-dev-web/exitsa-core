from dataclasses import dataclass
from utils.base_dto import BaseDto
from user.models import User


@dataclass
class UpdateUserDTO(BaseDto):
    first_name: str
    last_name: str
    email: str
    user_id: str
    user: User
    gender: str = None
    phone: str = None
    birthday: str = None
    second_last_name: str = None

