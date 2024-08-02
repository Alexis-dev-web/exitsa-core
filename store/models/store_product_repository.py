import uuid
from .store_has_product import StoreHasProduct


class StoreProductRepository:

    def get_by_id(self, id: uuid.uuid4) -> StoreHasProduct:
        return StoreHasProduct.objects.filter(id=id).first()

    def get_by_store_id_and_product_id(self, store_id: uuid.uuid4, product_id: uuid.uuid4) -> StoreHasProduct:
        return StoreHasProduct.objects.filter(store_id=store_id, product_id=product_id).first()

