from utils.basic_use_case import UseCase
from user.dto import CreateUserDTO
from user.models import User, GroupRepository


class UpdateUserUseCase(UseCase):

    def __init__(self) -> None:
        self.group_repository = GroupRepository()

    def execute(self, request: CreateUserDTO) -> User:
        user = request.user
        user.first_name = request.first_name
        user.last_name = request.last_name
        user.phone = request.phone
        user.second_last_name = request.second_last_name
        user.birthday = request.birthday
        user.gender = request.gender
        user.is_superuser = request.is_superuser

        user.save()
        
        if not request.group:
            request.group = self.group_repository.get_by_name('CLIENT')

        user.groups.set([request.group])

        return user
