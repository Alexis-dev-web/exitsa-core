from product.responses import ProductResponse
from product.models import AlertProduct


class AlertProductResponse:

    def __init__(self) -> None:
        self.product_response = ProductResponse()

    def to_json(self, alert: AlertProduct) -> dict:
        return {
            'id': str(alert.id),
            'min_quantity': alert.min_quantity,
            'is_default': alert.is_default,
            'is_active': alert.is_active,
            'created_at': str(alert.created_at),
            'updated_at': str(alert.created_at)
        }

    def with_product(self, alert: AlertProduct) -> dict:
        response = self.to_json(alert)
        response['product'] = self.product_response.to_json(alert.product)

        return response
