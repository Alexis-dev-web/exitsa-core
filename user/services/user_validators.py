from django.contrib.auth.models import Permission, Group

from user.models import UserRepository, User, PermissionRepository, GroupRepository
from utils.error_messages import messages
from rest_framework import serializers


class UserValidators:

    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.permission_repository = PermissionRepository()
        self.group_repository = GroupRepository()

    def validate_user_exist_by_id(self, user_id: str, message: str = messages['user_not_exist']) -> User:
        user = self.user_repository.get_by_id(user_id)
        
        if not user:
            raise serializers.ValidationError({'user': [message]})
        
        return  user

    def validate_perimission_exist(self, id: str) -> Permission:
        permission = self.permission_repository.get_by_id(id)

        if not permission:
            raise serializers.ValidationError({'permission': [messages['permission_not_exist']]})

        return permission

    def validate_group_already_exist_by_name(self, name: str) -> Group:
        group = self.group_repository.get_by_name(name)

        if group:
            raise serializers.ValidationError({'group': [messages['group_exist']]})

        return group

    def validate_can_not_create_super_user(self, user: User, value: bool) -> bool:
        if not user.is_superuser and value:
            serializers.ValidationError({'user': [messages['can_not_create_superuser']]})

        return value

    def validate_grup_exist(self, id: str) -> Group:
        group = self.group_repository.get_by_id(id)
        
        if not group:
            raise serializers.ValidationError({'group': [messages['group_not_exist']]})

        return group
