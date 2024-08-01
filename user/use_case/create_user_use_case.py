from utils.basic_use_case import UseCase
from user.dto import CreateUserDTO
from user.models import User

class CreateUserUseCase(UseCase):

    def execute(self, request: CreateUserDTO) -> User:
        user = User.objects._create_user(
            email=request.email,
            first_name=request.first_name,
            password=request.password,
            last_name=request.last_name,
            second_last_name=request.second_last_name,
            phone=request.phone,
            birthday=request.birthday,
            gender=request.gender
        )
        #TODO: SEND email new account and set new permissions 

        return user

