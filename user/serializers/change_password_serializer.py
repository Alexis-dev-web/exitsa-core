from rest_framework import serializers

from utils.error_messages import messages

from .get_user_serializer import GetUserSerializer


class ChangePasswordSerializer(GetUserSerializer):
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, data: dict) -> dict:
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError({'password': [messages['passwords_not_equal']]})

        return data

