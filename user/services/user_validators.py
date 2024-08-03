from user.models import UserRepository, User
from utils.error_messages import messages
from rest_framework import serializers


class UserValidators:

    def __init__(self) -> None:
        self.userRepository = UserRepository()

    def validate_user_exist_by_id(self, user_id: str, message: str = messages['user_not_exist']) -> User:
        user = self.userRepository.get_by_id(user_id)
        
        if not user:
            raise serializers.ValidationError(message)
        
        return  user

