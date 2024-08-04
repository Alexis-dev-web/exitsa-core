from rest_framework import serializers

from utils.serializers.base_paginate_serializer import BasePaginateSerializer


class OrderReportSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
