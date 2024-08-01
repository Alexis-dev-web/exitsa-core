import uuid

from rest_framework import serializers

from utils.error_messages import messages
from store.models import Store, StoreRepository


class StoreValidators:

    def __init__(self) -> None:
        self.store_repository = StoreRepository()

    def validate_store(self, id: uuid.uuid4) -> Store:
        store = self.store_repository.get_by_id(id)
        if not store:
            raise serializers.ValidationError({'store': messages['store_not_exist']})

        return store
