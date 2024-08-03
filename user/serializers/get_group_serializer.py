from rest_framework import serializers

from user.models import User
from user.services import UserValidators


class GetGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    group = serializers.SerializerMethodField('_validate_group')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()

    def _validate_group(self, data: dict) -> User:
        group_id = data.get('group_id', None)

        return self.user_validators.validate_grup_exist(group_id)

