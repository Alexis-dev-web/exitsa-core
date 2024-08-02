from product.models import Product


class ProductResponse:
    
    def to_json(self, product: Product) -> dict:
        return {
            'id': str(product.id),
            'sku': product.sku,
            'name': product.name,
            'description': product.description,
            'image_preview': product.image_preview,
            'type': product.type,
            'state': product.state,
            'base_pricing': product.base_pricing,
            'base_cost': product.base_cost,
            'in_existence': product.in_existence,
            'is_active': product.is_active,
            'created_at': str(product.created_at),
            'updated_at': str(product.created_at)
        }

