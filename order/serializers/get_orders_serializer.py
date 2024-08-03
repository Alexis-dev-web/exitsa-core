from rest_framework import serializers

from utils.error_messages import messages
from order.models import Order


class GetOrdersSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    limit = serializers.IntegerField(required=False, default=10)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    status = serializers.ChoiceField(Order.STATUS_CHOICE, required=False)
    type = serializers.ChoiceField(Order.TYPE_CHOICE, required=False)
    max_price = serializers.FloatField(required=False)
    min_price = serializers.FloatField(required=False)

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError({'date': messages['end_date_not_greater_start_date']})
        
        return data
