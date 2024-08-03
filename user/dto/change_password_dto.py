from dataclasses import dataclass
from utils.base_dto import BaseDto

from user.models import User


@dataclass
class ChangePasswordDTO(BaseDto):
    password: str
    user_id: str
    user: User
