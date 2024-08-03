from dataclasses import dataclass
from utils.base_dto import BaseDto

from user.models import User


@dataclass
class CreateUserDTO(BaseDto):
    first_name: str
    last_name: str
    email: str
    group: int
    user_id: str = None
    user: User = None
    gender: str = None
    phone: str = None
    birthday: str = None
    second_last_name: str = None
    password: str = None
    confirm_password: str = None
    is_superuser: bool = False

