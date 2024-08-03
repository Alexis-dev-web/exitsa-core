from rest_framework import serializers


class BasePaginateSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, max_value=100)
    limit = serializers.IntegerField(required=False, default=10)

