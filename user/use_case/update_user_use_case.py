from utils.basic_use_case import UseCase
from user.dto import UpdateUserDTO
from user.models import User


class UpdateUserUseCase(UseCase):

    def execute(self, request: UpdateUserDTO) -> User:
        user = request.user
        user.first_name = request.first_name
        user.last_name = request.last_name
        user.phone = request.phone
        user.second_last_name = request.second_last_name
        user.birthday = request.birthday
        user.gender = request.gender

        user.save()
        return user
