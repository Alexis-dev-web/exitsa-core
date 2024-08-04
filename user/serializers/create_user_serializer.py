from rest_framework import serializers

from utils.error_messages import messages

from .basic_user_serializer import BasicUserSerializer


class CreateUserSerializer(BasicUserSerializer):
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, data: dict) -> dict:
        email = data.get('email', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        request = self.context.get('request', None)
        is_superuser = data.get('is_superuser', False)
        group = data.get('group', None)

        if group:
            self.user_validators.validate_grup_exist(group)
        
        if request:
            self.user_validators.validate_can_not_create_super_user(request.user, is_superuser)

        if password != confirm_password:
            raise serializers.ValidationError({'password': [messages['passwords_not_equal']]})

        email_take = self.user_repository.get_by_email(email)
        if email_take:
            raise serializers.ValidationError({'email': [messages['user_exist']]})

        return data

