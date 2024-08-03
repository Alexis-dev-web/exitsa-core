from django.core.paginator import Paginator
from .user import User


class UserRepository:

    def get_by_email(self, email: str) -> User:
        return User.objects.filter(email=email).first()

    def get_by_id(self, id: str) -> User:
        return User.objects.filter(id=id).first()

    def get_all_paginate(self, limit: int = 10) -> Paginator:
        users = User.objects.all().order_by('created_at')
        paginator = Paginator(users, limit)

        return paginator

    def get_by_email_paginate(self, email:str, limit: int = 10) -> Paginator:
        users = User.objects.filter(email__icontains=email).order_by('created_at')
        paginator = Paginator(users, limit)

        return paginator

    def get_by_gender_paginate(self, gender: str, limit: int = 10) -> Paginator:
        users = User.objects.filter(gender=gender).order_by('created_at')
        paginator = Paginator(users, limit)

        return paginator
