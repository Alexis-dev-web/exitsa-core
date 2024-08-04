from utils.basic_use_case import UseCase
from user.dto import CreateUserDTO
from user.models import User, GroupRepository

class CreateUserUseCase(UseCase):

    def __init__(self) -> None:
        self.group_repository = GroupRepository()

    def execute(self, request: CreateUserDTO) -> User:
        user = User.objects._create_user(
            email=request.email,
            first_name=request.first_name,
            password=request.password,
            last_name=request.last_name,
            second_last_name=request.second_last_name,
            phone=request.phone,
            birthday=request.birthday,
            gender=request.gender,
            is_superuser=request.is_superuser if request.origin == 'ADMIN' else False
        )

        if not request.group:
            request.group = self.group_repository.get_by_name('CLIENT')

        user.groups.set([request.group])
        #TODO: SEND email new account and set new permissions 

        return user

