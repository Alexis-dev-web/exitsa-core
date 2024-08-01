import uuid
from .store import Store


class StoreRepository:

    def get_all(self) -> list[Store]:
        return Store.objects.all()

    def get_by_name(self, name: str) -> Store:
        return Store.objects.filter(name=name).first()

    def get_by_id(self, id: uuid.uuid4) -> Store:
        return Store.objects.filter(id=id).first()