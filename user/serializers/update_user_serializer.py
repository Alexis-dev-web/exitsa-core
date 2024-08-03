from rest_framework import serializers

from utils.error_messages import messages

from user.models import User
from .basic_user_serializer import BasicUserSerializer


class UpdateUserSerializer(BasicUserSerializer):
    user_id = serializers.UUIDField()
    user = serializers.SerializerMethodField('_validate_user')

    def _validate_user(self, data: dict) -> User:
        email = data.get('email', None)
        user_id = data.get('user_id', None)
        
        user = self.user_validators.validate_user_exist_by_id(user_id)
        
        email_exits = self.user_repository.get_by_email(email)

        if email_exits and email_exits.id != user_id:
            raise serializers.ValidationError({'user': [messages['user_exist']]})

        return user
        
    def validate(self, data):
        request = self.context.get('request')
        is_superuser = data.get('is_superuser', False)

        self.user_validators.validate_can_not_create_super_user(request.user, is_superuser)
        return data

