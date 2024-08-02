from store.models import StoreHasProduct


class StoreProductResponse:
    
    def to_json(self, store_product: StoreHasProduct) -> dict:
        return {
            'id': str(store_product.id),
            'is_sould_out': store_product.is_sould_out,
            'current_price': store_product.current_price,
            'product_id': str(store_product.product.id),
            'store_id': str(store_product.store.id),
            'created_at': str(store_product.created_at),
            'updated_at': str(store_product.updated_at)
        }

