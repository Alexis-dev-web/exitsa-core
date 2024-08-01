from rest_framework import serializers

from utils.error_messages import messages
from store.models import Store
from store.services import StoreValidators
from utils.utils import validate_url


class UpdatetoreSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, required=False)
    type = serializers.ChoiceField(Store.STORE_CHOICE)
    url = serializers.CharField(max_length=255, required=False)
    store_id = serializers.UUIDField()
    store = serializers.SerializerMethodField('_validate_store')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.store_validator = StoreValidators()

    def _validate_store(self, data: dict) -> Store:
        store_id = data.get('store_id', None)
        name = data.get('name', None)

        store = self.store_validator.validate_store(store_id)

        store_exist = self.store_validator.store_repository.get_by_name(name.upper())
        if store_exist and store_exist.id != store.id:
            raise serializers.ValidationError({'store': messages['store_exist']})

        return store

    def validate(self, data: dict) -> str:
        url = data.get('url', None)

        if url and not validate_url(url):
            raise serializers.ValidationError({'url': messages['invalid_url']})

        return data
