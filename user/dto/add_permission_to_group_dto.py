from dataclasses import dataclass
from utils.base_dto import BaseDto
from django.contrib.auth.models import Group, Permission

@dataclass
class AddPermisionToGroupDTO(BaseDto):
    permission_id: str
    permission: Permission
    group_id: str = None
    group: Group = None
