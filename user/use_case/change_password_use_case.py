from utils.basic_use_case import UseCase

from user.dto import ChangePasswordDTO
from user.models import User


class ChangePasswordUseCase(UseCase):

    def execute(self, request: ChangePasswordDTO) -> User:
        user = request.user
        user.set_password(request.password)

        user.save()

        return request.user
