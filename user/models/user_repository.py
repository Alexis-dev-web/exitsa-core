import uuid

from .user import User


class UserRepository:

    def get_by_email(self, email: str) -> User:
        return User.objects.filter(email=email).first()

    def get_by_id(self, id: uuid.UUID) -> User:
        return User.objects.filter(id=id)
