from rest_framework import serializers
from django.contrib.auth.models import Group
from utils.error_messages import messages

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
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    is_superuser = serializers.BooleanField()

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()
        self.user_repository = UserRepository()

