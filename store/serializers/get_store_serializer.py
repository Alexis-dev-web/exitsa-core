from rest_framework import serializers

from store.models import Store
from store.services import StoreValidators


class GetStoreSerializer(serializers.Serializer):
    store_id = serializers.UUIDField()
    store = serializers.SerializerMethodField('_validate_store')

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.store_validator = StoreValidators()

    def _validate_store(self, data: dict) -> Store:
        store_id = data.get('store_id', None)

        return self.store_validator.validate_store(store_id)
