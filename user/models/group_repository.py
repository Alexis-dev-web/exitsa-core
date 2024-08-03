from django.core.paginator import Paginator
from django.contrib.auth.models import Group


class GroupRepository:

    def get_by_name(self, name: str) -> Group:
        return Group.objects.filter(name=name).first()

    def get_all_paginate(self, limit: int = 10) -> Paginator:
        groups = Group.objects.all()
        paginator = Paginator(groups, limit)

        return paginator

    def get_by_id(self, id: str) -> Group:
        return Group.objects.filter(id=id).first()
