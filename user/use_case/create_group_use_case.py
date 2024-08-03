from django.contrib.auth.models import Group
from utils.basic_use_case import UseCase

from user.dto import CreateGroupDTO
from user.response import GroupResponse


class CreateGroupUseCase(UseCase):

    def __init__(self) -> None:
        self.group_response = GroupResponse()

    def execute(self, request: CreateGroupDTO) -> dict:
        group = Group()
        group.name = request.group

        group.save()

        group.permissions = group.permissions.set(request.permissions)

        return self.group_response.to_json(group)
