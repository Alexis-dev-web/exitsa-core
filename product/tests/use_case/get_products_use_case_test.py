from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest

from product.tests.product_dummy import ProductDummy
from product.dto import GetProductsDTO
from product.use_case import GetProductsUseCase


class GetProductsUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = ProductDummy()
        self.get_product_use_case = GetProductsUseCase()

    @patch('product.models.ProductRepository.get_paginate')
    def test_get_products(self, mock_products):
        products = self.dummy_data.build_paginator_products()
        products_dto = GetProductsDTO()
        #mock 
        mock_products.return_value = products

        response = self.get_product_use_case.execute(products_dto)

        self.assertEqual(3, len(response['items']))
