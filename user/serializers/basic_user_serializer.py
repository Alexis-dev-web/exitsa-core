from rest_framework import serializers
from django.contrib.auth.models import Group

from user.models import User, UserRepository, GroupRepository
from user.services import UserValidators


class BasicUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    second_last_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(max_length=255)
    phone = serializers.CharField(max_length=10, required=False)
    birthday = serializers.DateField(required=False)
    gender = serializers.ChoiceField(User.GENDER)
    is_superuser = serializers.BooleanField(required=False, default=False)
    group = serializers.IntegerField(required=False)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()
        self.user_repository = UserRepository()

