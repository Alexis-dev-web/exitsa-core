from rest_framework import serializers

from django.contrib.auth.models import Permission
from user.services import UserValidators

from .add_permission_to_group_serializer import AddPermissionToGroupSerializer


class CreateGroupSerializer(serializers.Serializer):
    group = serializers.CharField(max_length=100)
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_validators = UserValidators()

    def validate(self, data: dict) -> Permission:
        group = data.get('group', None)

        self.user_validators.validate_group_already_exist_by_name(group)

        return data
