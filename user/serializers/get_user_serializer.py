from rest_framework import serializers

from user.models import User
from user.services import UserValidators


class GetUserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    user = serializers.SerializerMethodField('_validate_user')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()

    def _validate_user(self, data: dict) -> User:
        user_id = data.get('user_id', None)

        return self.user_validators.validate_user_exist_by_id(user_id)

