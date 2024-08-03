from utils.basic_use_case import UseCase

from utils.response.paginate_response import PaginateResponse
from user.dto import GetUsersDTO
from user.models import UserRepository
from user.response import UserResponse


class GetUsersUseCase(UseCase):

    def __init__(self) -> None:
        self.paginate_response = PaginateResponse()
        self.user_response = UserResponse()
        self.user_repository = UserRepository()

    def execute(self, request: GetUsersDTO) -> dict:
        if not request.email and not request.gender:
            users = self.user_repository.get_all_paginate(request.limit)

        if request.email:
            users = self.user_repository.get_by_email_paginate(request.email, request.limit)
        elif request.gender:
            users = self.user_repository.get_by_gender_paginate(request.email, request.limit)

        page = users.page(request.page)

        items = [self.user_response.to_json(user) for user in page.object_list or []]

        return self.paginate_response.to_json(page, users.num_pages, users.count, items)

