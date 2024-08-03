from rest_framework import serializers

from user.models import User
from utils.serializers.base_paginate_serializer import BasePaginateSerializer


class GetUsersSerializer(BasePaginateSerializer):
    email = serializers.CharField(required=False)
    gender = serializers.ChoiceField(User.GENDER, required=False)
