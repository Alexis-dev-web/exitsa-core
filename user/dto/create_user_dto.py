from dataclasses import dataclass
from utils.base_dto import BaseDto


@dataclass
class CreateUserDTO(BaseDto):
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str
    gender: str = None
    phone: str = None
    birthday: str = None
    second_last_name: str = None

