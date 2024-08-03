from django.contrib.auth.models import Permission


class PermissionRepository:

    def get_by_id(self, id: str) -> Permission:
        return Permission.objects.filter(id=id).first()
    

