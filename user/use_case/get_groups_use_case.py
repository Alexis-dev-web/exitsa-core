from django.contrib.auth.models import Group
from utils.basic_use_case import UseCase

from utils.response.paginate_response import PaginateResponse
from utils.dto.paginate_base_dto import PaginateBaseDTO

from user.models import GroupRepository
from user.response import GroupResponse


class GetGroupsUseCase(UseCase):

    def __init__(self) -> None:
        self.group_response = GroupResponse()
        self.group_repository = GroupRepository()
        self.paginate_response = PaginateResponse()

    def execute(self, request: PaginateBaseDTO ) -> dict:
        groups = self.group_repository.get_all_paginate(request.limit)

        page = groups.page(request.page)

        items = [self.group_response.get_group_with_permission(group) for group in page.object_list or []]

        return self.paginate_response.to_json(page, groups.num_pages, groups.count, items)

