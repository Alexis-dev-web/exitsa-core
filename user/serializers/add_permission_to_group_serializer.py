from rest_framework import serializers

from django.contrib.auth.models import Permission
from user.services import UserValidators

from utils.error_messages import messages


class AddPermissionToGroupSerializer(serializers.Serializer):
    permission_id = serializers.IntegerField()
    permission = serializers.SerializerMethodField('_validate_permission')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()

    def _validate_permission(self, data: dict) -> Permission:
        permission_id = data.get('permission_id')

        permission = self.user_validators.validate_perimission_exist(permission_id)

        return permission
