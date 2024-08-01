from rest_framework import serializers

from utils.error_messages import messages

from user.models import User
from .create_user_serializer import CreateUserSerializer


class UpdateUserSerializer(CreateUserSerializer):
    user_id = serializers.UUIDField()
    password = serializers.CharField(max_length=255, required=False)
    confirm_password = serializers.CharField(max_length=255, required=False)
    user = serializers.SerializerMethodField('_validate_user')

    def _validate_user(self, data: dict) -> User:
        email = data.get('email', None)
        user_id = data.get('user_id', None)
        
        user = self.user_validators.validate_user_exist_by_id(user_id)
        
        email_exits = self.user_repository.get_by_email(email)

        if email_exits and user.id != user_id:
            raise serializers.ValidationError(messages['user_exist'])

        return user
        
    def validate(self, data):
        return data

