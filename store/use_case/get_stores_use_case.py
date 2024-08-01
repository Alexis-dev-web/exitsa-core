from utils.basic_use_case import UseCase
from store.models import StoreRepository
from store.response import StoreResponse


class GetStoresUseCase(UseCase):

    def __init__(self) -> None:
        self.store_response = StoreResponse()
        self.store_repository = StoreRepository()

    def execute(self) -> list[dict]:
        stores = self.store_repository.get_all()

        return [self.store_response.to_json(store) for store in stores or []]

