from django.contrib.auth.models import Group, Permission


class GroupResponse:

    def to_json(self, group: Group) -> dict:
        return {
            'id': group.pk,
            'name': group.name
        }

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
