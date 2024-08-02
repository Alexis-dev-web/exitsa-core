import uuid

from rest_framework import serializers

from utils.error_messages import messages
from product.models import Product, ProductRepository


class ProductValidators:
    
    def __init__(self) -> None:
        self.product_repository = ProductRepository()

    def validate_product_exist_by_id(self, id: uuid.uuid4) -> Product:
        product = self.product_repository.get_by_id(id)
        if not product:
            raise serializers.ValidationError({'product': messages['product_not_exist']})

        return product

