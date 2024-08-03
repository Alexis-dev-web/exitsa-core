from rest_framework import serializers

from user.models import User, UserRepository
from user.services import UserValidators


class BasicUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    second_last_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(max_length=255)
    phone = serializers.CharField(max_length=10, required=False)
    birthday = serializers.DateField(required=False)
    gender = serializers.ChoiceField(User.GENDER)
    group = serializers.CharField(max_length=255)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()
        self.user_repository = UserRepository()

