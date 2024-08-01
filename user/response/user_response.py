from user.models import User


class UserResponse:

    def to_json(self, user: User) -> dict:
        return {
            'id': str(user.id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'second_last_name': user.second_last_name,
            'email': user.email,
            'phone': user.phone,
            'birthday': user.birthday,
            'gender': user.gender,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'last_login': str(user.last_login),
            'created_at': str(user.created_at),
            'updated_at': str(user.updated_at),
            'deleted_at': str(user.deleted_at)
        }

