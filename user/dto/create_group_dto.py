from dataclasses import dataclass, field
from utils.base_dto import BaseDto

from .add_permission_to_group_dto import AddPermisionToGroupDTO
from user.serializers import AddPermissionToGroupSerializer


@dataclass
class CreateGroupDTO(BaseDto):
    group: str
    permissions: list = field(default_factory=list)

    # def __post_init__(self):
    #     self.permissions = [AddPermisionToGroupDTO.from_json(permission) for permission in self.permissions or []]
