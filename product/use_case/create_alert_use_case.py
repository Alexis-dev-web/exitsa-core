from utils.basic_use_case import UseCase

from product.dto import AlertProductDTO
from product.models import AlertProduct, AlertProductRepository
from product.responses import AlertProductResponse


class CreateAlertProductUseCase(UseCase):
    
    def __init__(self) -> None:
        self.alert_product_repository = AlertProductRepository()
        self.alert_product_response = AlertProductResponse()

    def execute(self, request: AlertProductDTO) -> dict:
        if request.is_default:
            default = self.alert_product_repository.get_default()
            if default:
                default.is_active = False
                default.save()
    
        alert_product = self.alert_product_repository.get_by_product(request.product_id)
        if alert_product:
            alert_product.is_active = False
            alert_product.save()

        alert = AlertProduct()
        alert.min_quantity = request.min_quantity
        alert.product = request.product
        alert.is_active = request.is_active
        alert.is_default = request.is_default

        alert.save()        

        return self.alert_product_response.to_json(alert)
