from utils.basic_use_case import UseCase

from store.dto import AddProductToStoreDTO
from store.models import StoreHasProduct


class AddProductToStoreUseCase(UseCase):

    def execute(self, request: AddProductToStoreDTO) -> StoreHasProduct:
        store_product = StoreHasProduct()
        store_product.current_price = request.current_price if request.current_price else request.product.base_pricing
        store_product.is_sould_out = request.is_sould_out
        store_product.store = request.store
        store_product.product = request.product

        store_product.save()
        
        return store_product

