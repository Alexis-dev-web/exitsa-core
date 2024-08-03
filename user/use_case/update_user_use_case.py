from utils.basic_use_case import UseCase
from user.dto import CreateUserDTO
from user.models import User


class UpdateUserUseCase(UseCase):

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
        
        user.groups.set([request.group])

        return user
