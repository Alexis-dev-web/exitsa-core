from utils.basic_use_case import UseCase

from product.models import Product, AlertProductRepository


class UpdateInventoryProductUseCase(UseCase):

    def __init__(self) -> None:
        self.alert_product_repository = AlertProductRepository()

    def execute(self, product: Product, transaction: str, quantity: int, status: str):
        if transaction == 'BUY' and (status != 'REJECTED' or status != 'CANCELLED'):
            product.in_existence += quantity

            if status == 'SENT':
                product.state = 'REFILLING'
        elif transaction == 'SALE':
            if status == 'CANCELLED':
                product.in_existence += quantity
                product.save()
                return False, None

            if quantity >= product.in_existence:
                return False, None

            product.in_existence -= quantity

        product.state = 'SOULD_OUT' if product.in_existence == 0 else 'IN_STOCK'

        product.save()

        alert = self.alert_product_repository.get_by_product(product.id)
        if not alert:
            alert = self.alert_product_repository.get_default()

        if alert and product.in_existence <= alert.min_quantity:
            #TODO: Create notification
            notification = []

        return True, None
