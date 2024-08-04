import uuid

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from user.models import User


class UserDummyData:

    def build_user_test(self, email='testing@exitosa.test'):
        user = User()
        user.first_name = 'test'
        user.last_name = 'Smith'
        user.email = email
        user.is_superuser = True

        return user

    def build_basic_request(self) -> dict:
        return {
            'first_name': 'test',
            'last_name': 'Smitch',
            'email': 'testing@exitosa.test',
            'password': 'newPassword',
            'confirm_password': 'newPassword',
            'gender': 'M'
        }

    def request_args_get(self) ->dict:
        return {
            'page': 1,
            'limit': 10,
        }

    def request_change_password(self, user_id: str = uuid.uuid4()) -> dict:
        return {
            'user_id': str(user_id),
            'password': 'newPassword',
            'confirm_password': 'newPassword',
        }

    def basic_group(self):
        group = Group()
        group.name = 'New group'

        return group

    def dict_create_group(self) -> dict:
        return {
            'group': 'ADMINS',
            'permissions': [1]
        }

    def build_permission(self):
        permission = Permission()
        permission.name = 'New permission'
        permission.codename = 'new_permisison'
        permission.content_type = ContentType.objects.get_for_model(User)

        return permission
