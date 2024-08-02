import uuid

from rest_framework import serializers

from utils.error_messages import messages
from store.models import Store, StoreRepository, StoreHasProduct, StoreProductRepository


class StoreValidators:

    def __init__(self) -> None:
        self.store_repository = StoreRepository()
        self.store_product_repository = StoreProductRepository()

    def validate_store(self, id: uuid.uuid4) -> Store:
        store = self.store_repository.get_by_id(id)
        if not store:
            raise serializers.ValidationError({'store': messages['store_not_exist']})

        return store

    def validate_exist_product_in_store(self, store_id: uuid.uuid4, product_id: uuid.uuid4) -> StoreHasProduct:
        store_product = self.store_product_repository.get_by_store_id_and_product_id(store_id, product_id)
        if store_product:
            raise serializers.ValidationError({'product': messages['product_already_assign']})
