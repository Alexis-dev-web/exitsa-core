from rest_framework import serializers


from utils.error_messages import messages
from .add_product_serializer import AddProductSerializer

from user.models import User
from user.services import UserValidators
from store.models import Store
from store.services import StoreValidators
from order.models import Order


class OrderSerializer(serializers.Serializer):
    total_price = serializers.IntegerField(required=False)
    is_paid = serializers.BooleanField(required=False, default=False)
    date_pay = serializers.DateField(required=False)
    client_id = serializers.CharField(max_length=255, required=False)
    type = serializers.ChoiceField(Order.TYPE_CHOICE)
    store_id = serializers.CharField(max_length=255, required=False)
    delivered_date = serializers.DateField(required=False)
    products = serializers.ListField(child=AddProductSerializer(), required=False)
    store = serializers.SerializerMethodField('_validate_store')
    client = serializers.SerializerMethodField('_validate_client')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.store_validators = StoreValidators()
        self.user_validator = UserValidators()

    def _validate_client(self, data: dict) -> User:
        client = None
        type = data.get('type')
        client_id = data.get('client_id', None)

        if type == 'SALE' and not client_id: 
            raise serializers.ValidationError({'client_id': [messages['client_id_required']]})

        if client_id:
            client = self.user_validator.validate_user_exist_by_id(client_id, messages['client_not_exists'])

        return client

    def _validate_seller(self, data: dict) -> User:
        seller = None
        seller_id = data.get('seller_id', None)

        if seller_id:
            seller = self.user_validator.validate_user_exist_by_id(seller_id, messages['seller_not_exists'])

        return seller

    def _validate_store(self, data: dict) -> Store:
        store = None
        store_id = data.get('store_id', None)
        type = data.get('type')
        
        if type == 'BUY' and not store_id: 
            raise serializers.ValidationError({'store_id': [messages['store_id_required']]})

        if store_id:
            store = self.store_validators.validate_store(store_id)

        return store

    def validate(self, data: dict) -> dict:
        is_paid = data.get('is_paid')
        date_paid = data.get('date_paid', False)

        if is_paid and not date_paid:
            raise serializers.ValidationError({'date_paid': [messages['date_paid_required']]})
        
        return data

