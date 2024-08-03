import uuid

from user.models import User
from django.contrib.auth.models import Group


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
            'gender': 'M',
            'group': 1
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
