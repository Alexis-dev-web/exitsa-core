from rest_framework import serializers

from utils.error_messages import messages

from user.models import User, UserRepository
from user.services import UserValidators


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    second_last_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255, required=False)
    birthday = serializers.DateField(required=False)
    gender = serializers.ChoiceField(User.GENDER)
    group = serializers.CharField(max_length=255)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()
        self.user_repository = UserRepository()

    def validate(self, data: dict) -> dict:
        email = data.get('email', None)
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError(messages['passwords_not_equal'])

        email_take = self.user_repository.get_by_email(email)
        if email_take:
            raise serializers.ValidationError(messages['user_exist'])

        return data

