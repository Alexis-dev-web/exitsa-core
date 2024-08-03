from rest_framework import serializers

from utils.error_messages import messages
from store.models import Store, StoreRepository
from utils.utils import validate_url


class CreateStoreSerializer(serializers.Serializer):
    is_provider = serializers.BooleanField(required=False)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, required=False)
    type = serializers.ChoiceField(Store.STORE_CHOICE)
    url = serializers.CharField(max_length=255, required=False)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.store_repository = StoreRepository()

    def validate(self, data: dict) -> dict:
        name: str = data.get('name', None)
        url = data.get('url', None)

        if url and not validate_url(url):
            raise serializers.ValidationError({'url': messages['invalid_url']})

        store = self.store_repository.get_by_name(name.upper())
        if store:
            raise serializers.ValidationError({'store': messages['store_exist']})

        return data

