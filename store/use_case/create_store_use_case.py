from utils.basic_use_case import UseCase

from store.dto import CreateOrUpdateStoreDTO
from store.models import Store


class CreateOrUpdateStoreUseCase(UseCase):

    def execute(self, request: CreateOrUpdateStoreDTO) -> Store:
        store = Store() if not request.store else request.store
        store.name = request.name.upper()
        store.description = request.description
        store.url = request.url
        store.type = request.type
        store.is_provider = request.is_provider

        store.save()

        return store

