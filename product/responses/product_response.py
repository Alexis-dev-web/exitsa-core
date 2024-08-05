from product.models import Product, AlertProduct


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

    def with_alert(self, product: Product, alert: dict = {}) -> dict:
        response = self.to_json(product)
        response['alert'] = alert

        return response
