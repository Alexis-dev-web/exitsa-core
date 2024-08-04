from utils.base_response import BaseResponseModel
from django.contrib.auth.models import Group, Permission


class GroupResponse(BaseResponseModel):

    def permission_to_json(self, permission: Permission) -> dict:
        return {
            'id': permission.pk,
            'name': permission.name,
            'code': permission.codename  
        }

    def get_group_with_permission(self, group: Group) -> dict:
        response = self.to_json(group)

        response['permissions'] = [self.permission_to_json(permission) for permission in group.permissions.all() or []]

        return response
